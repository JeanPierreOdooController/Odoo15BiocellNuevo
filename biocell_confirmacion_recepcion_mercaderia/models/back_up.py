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
					ol.append(acol.id)
			if ac.order_line_stock:
				for acols in ac.order_line_stock:
					ols.append(acols.id)
			for odlns in ac.order_line_stock:
				# raise UserError('ingreso')
				existe = self.env["sale.order.line"].sudo().search([("order_id","=",self.id),("product_id","=",int(odlns.product_id.id)),('sale_type','!=','stock')],limit=1)
				# existe = self.env["sale.order.line"].sudo().search([("order_id","=",self.id),("product_id","=",int(odlns.product_id.id)),('sale_type','!=','stock'),('tax_id','=',odlns.tax_id),('analytic_tag_ids','=',odlns.analytic_tag_ids)],limit=1)
				if existe.id:
					if existe.product_uom_qty < odlns.product_uom_qty:
						existe.product_uom_qty = odlns.product_uom_qty
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
						'confirm_it': True
					}) 
		res = super().action_confirm()
		return res


	def action_cancel(self):
		for ain in self.order_line:
			ain.confirm_it = False
		res1 =super(SaleOrder, self).action_cancel()
		return res1