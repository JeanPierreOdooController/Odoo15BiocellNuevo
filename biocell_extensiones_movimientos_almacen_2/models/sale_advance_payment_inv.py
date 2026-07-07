# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class SaleAdvancePaymentInv(models.TransientModel):
	_inherit = 'sale.advance.payment.inv'

	def create_invoices(self):
		Sale = self.env['sale.order'].browse(self._context.get('active_id', False))
		before_invoices = Sale.invoice_ids
		res = super(SaleAdvancePaymentInv, self).create_invoices()
		after_invoices = Sale.invoice_ids
		new_invoice = after_invoices - before_invoices
		if len(new_invoice) == 1:
			productos = {}
			if self.picking_ids.ids:
				for line_picking in self.picking_ids.mapped('move_ids_without_package'):
					if line_picking.state == 'done':
						if line_picking.product_id.id in productos:
							productos[line_picking.product_id.id] = productos[line_picking.product_id.id] + line_picking.quantity_done
						else:
							productos[line_picking.product_id.id] = line_picking.quantity_done

				# for line_invoice in new_invoice.invoice_line_ids:
				# 	if line_invoice.product_id.type != 'service':

				# 		if line_invoice.product_id.id in productos and line_invoice.quantity > productos[line_invoice.product_id.id]:
				# 			line_invoice.quantity = productos[line_invoice.product_id.id]
				# 		elif line_invoice.product_id.id in productos:
				# 			pass
				# 		else:
				# 			line_invoice.unlink()
				# new_invoice._onchange_invoice_line_ids()
				for line_invoice in new_invoice.invoice_line_ids:
					if line_invoice.product_id.type != 'service':
						product_id = line_invoice.product_id.id

						if product_id in productos:
							if line_invoice.quantity > productos[product_id]:
								line_invoice.quantity = productos[product_id]

							# Buscar los lotes desde stock.move.line
							lot_names = set()
							for picking in self.picking_ids:
								for move in picking.move_ids_without_package.filtered(lambda m: m.product_id.id == product_id):
									for move_line in move.move_line_ids.filtered(lambda l: l.lot_id):
										if move_line.lot_id.use_expiration_date:
											lot_names.add(move_line.lot_id.name + " F.V.: " + str(move_line.lot_id.expiration_date.date()))
										else:
											lot_names.add(move_line.lot_id.name)

							# Si hay lotes, agregar al campo name
							if lot_names:
								lot_str = ", ".join(sorted(lot_names))
								# Evitar agregar repetido si se vuelve a llamar
								if f"Lote:" not in line_invoice.name:
									line_invoice.name += f"{line_invoice.name or ''}\nLote: {lot_str}"
		return res
