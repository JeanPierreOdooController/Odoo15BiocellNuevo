# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
from datetime import *
from datetime import timedelta

class account_move(models.Model):
	_inherit = 'account.move'

	purchase_ebill = fields.Char('Origen - Nro. de Compra',compute="get_purchase_ebill")

	def get_purchase_ebill(self):
		for i in self:
			alltext = ""
			if self.env.company.origen_nro_compra != False:
				for l in i.invoice_line_ids:
					for m in l.sale_line_ids:
						if m.id and m.order_id.id and m.order_id.client_order_ref:
							alltext = m.order_id.client_order_ref
			i.purchase_ebill = alltext


	def get_lot_name(self):
		for i in self:
			if self.env.company.etiqueta_lote != False:			
				for lines in i.invoice_line_ids:
					if lines.lot_ids:
						if "\nLotes:\n" in lines.name:
							posicion = lines.name.find("\nLotes:\n")
							no_lote = lines.name[:posicion]
							lines.name = no_lote
							lines.name = (no_lote if no_lote else '') + "\nLotes:\n"
							for xx in lines.lot_ids.split('; '):
								lines.name += "(" + xx + ")\n"
							lines.name = lines.name[:-1]
						else:
							lines.name = (lines.name if lines.name else '') + "\nLotes:\n"
							for xx in lines.lot_ids.split('; '):
								lines.name += "(" + xx + ")\n"
							lines.name = lines.name[:-1]

	def write(self,vals):
		res = super(account_move, self).write(vals)
		for i in self:
			i.get_lot_name()
		return res

	@api.model
	def create(self,vals):
		t = super(account_move,self).create(vals)
		t.get_lot_name()
		return t



class stock_picking(models.Model):
	_inherit = 'stock.picking'

	nro_guia_compra = fields.Char(u'Nro. de Guía Remisión')

	def write(self,vals):
		t = super(stock_picking,self).write(vals)
		if self.invoice_id.id and 'invoice_id' in vals:
			self.invoice_id.refresh()
			self.invoice_id.get_lot_name()
		return t


class stock_move(models.Model):
	_inherit = 'stock.move'


	def write(self,vals):
		t = super(stock_move,self).write(vals)
		for i in self:
			if i.state  == 'done' and 'state' in vals:
				textd = ""
				for det in i.move_line_ids:
					if det.lot_id.id:
						if self.env.company.descript_move_l != False:
							textd += det.lot_id.name if textd == "" else ( ", " + det.lot_id.name)
						if self.env.company.fecha_caducidad != False:
							textd += " *Caducidad: " + str(det.lot_id.expiration_date or '')[:10] 

				if textd and i.description_picking  and (" - Lotes: " + textd) in i.description_picking:
					pass
				else:
					i.description_picking = (i.description_picking if i.description_picking else "") + ((" - Lotes: " + textd) if textd != "" else "")
		return t


class account_move_line(models.Model):
	_inherit = 'account.move.line'

	lot_ids = fields.Char('Lotes',compute="get_lot_ids")

	def get_lot_ids(self):
		for i in self:
			alltext = ""
			for l in i.sale_line_ids:
				for nm in l.move_ids:
					for m in nm.move_line_ids:
						if m.lot_id.id and nm.picking_id.invoice_id.id == i.move_id.id:
							texto = "LT. " + (m.lot_id.name or '') + " - Q. " +   str(m.qty_done)  + " - FV. " + str(m.lot_id.expiration_date or '')[:10] 
							alltext += texto if alltext== "" else ("; " + texto)
			i.lot_ids = alltext
