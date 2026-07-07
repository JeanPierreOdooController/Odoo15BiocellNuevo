# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from itertools import groupby
import json

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty

from odoo.addons.payment import utils as payment_utils

class SaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	confirm_old_id = fields.Many2one('sale.order.line', 'Empate Antiguo')
	state_old_confirm = fields.Selection([('01','Sale'),('02','Kardex')], 'Empate Antiguo', default='01')


	# def _old_confirm_it_sasfasd(self):
	# 	for sol in self:


class SaleOrder(models.Model):
	_inherit = "sale.order"



	def action_confirm(self):
		for ac in self:
			ol = []
			ols = []
			oln = []
			olns = []
			if ac.order_line:
				for acol in ac.order_line:
					acol.confirm_it = True



			for odlh in ac.order_line:
				if not odlh.quant_id:
					ex = self.env["sale.order.line"].sudo().search([("order_id","=",self.id),("product_id","=",int(odlh.product_id.id)),('sale_type','!=','stock'),('id','!=',int(odlh.id))],limit=1)
					if ex.id:
						if ex.product_uom_qty < odlh.product_uom_qty:
							odlh.product_uom_qty = ex.product_uom_qty
							ol.append(ex)
			seen_products = set()
			for a1 in ol:
				# un = self.env["sale.order.line"].sudo().search([("order_id","=",self.id),('id','=',int(a1))])
				if a1.product_id.id in seen_products:
					pass
				else:
					if a1.id:
						oln.append(a1)
					seen_products.add(a1.product_id.id)
			for a2 in oln:
				if a2.id:
					a2.unlink()

			for odlns in ac.order_line_stock:
				existe = self.env["sale.order.line"].sudo().search([
					("order_id", "=", self.id),
					("product_id", "=", int(odlns.product_id.id)),
					('sale_type', '!=', 'stock')
				], limit=1)

				if existe.id:
					# Realiza la consulta ORM para obtener el valor máximo de product_uom_qty para el producto actual
					product_id = existe.product_id.id
					max_product_uom_qty = self.env['sale.order.line'].sudo().search_read(
						domain=[('product_id', '=', product_id), ('sale_type', '!=', 'sale'), ("order_id_stock", "=", self.id)],
						fields=['product_uom_qty'],
						order='product_uom_qty desc',  # Ordena los registros por product_uom_qty en orden descendente
						limit=1  # Obtiene solo el registro con el valor máximo
					)
					
					if max_product_uom_qty:
						max_quantity = max_product_uom_qty[0].get('product_uom_qty', 0)
						if existe.product_uom_qty < max_quantity:
							existe.product_uom_qty = max_quantity
					existe.state_old_confirm = '02'
					existe.confirm_old_id = odlns.id
					# raise UserError(f'{total_product_uom_qty} sasy el id es {self.id}')
				else:					
					order_line_origin_2 = self.env['sale.order.line'].sudo().create({
						'order_id': self.id,
						'name': odlns.name,
						# 'sequence':odlns.sequence,
						'price_unit': odlns.price_unit,
						'price_subtotal': odlns.price_subtotal,
						'price_tax': odlns.price_tax,
						'price_total': odlns.price_total,
						'price_reduce': odlns.price_reduce,
						'tax_id': odlns.tax_id,
						'price_reduce_taxinc': odlns.price_reduce_taxinc,
						'price_reduce_taxexcl': odlns.price_reduce_taxexcl,
						'discount': odlns.discount,
						'product_id': odlns.product_id.id,
						'product_uom_qty': odlns.product_uom_qty,
						'product_uom': odlns.product_uom.id,
						'product_uom_category_id': odlns.product_uom_category_id.id,
						'product_uom_readonly': odlns.product_uom_readonly,
						'analytic_tag_ids': odlns.analytic_tag_ids,
						'is_expense': odlns.is_expense,
						'is_downpayment': odlns.is_downpayment,
						'customer_lead': odlns.customer_lead,
						'display_type': odlns.display_type,
						'product_packaging_id': odlns.product_packaging_id.id,
						'product_packaging_qty': odlns.product_packaging_qty,
						'sale_type':'sale',
						'confirm_it': True,
						'confirm_old_id': odlns.id,
						'sale_order_template_id': odlns.sale_order_template_id.id,
						'state_old_confirm': '02',
					}) 
			for un2 in ac.order_line:
				exun = self.env["sale.order.line"].sudo().search([("order_id","=",self.id),('display_type','=','line_section')])
				for unl2 in exun:
					if unl2.id:
						unl2.unlink()

		# raise UserError('ingreso 2222 ')
		res = super().action_confirm()
		return res


	def action_cancel(self):
		for ain in self.order_line:
			ain.confirm_it = False
		res1 =super(SaleOrder, self).action_cancel()
		return res1



	# def action_draft()