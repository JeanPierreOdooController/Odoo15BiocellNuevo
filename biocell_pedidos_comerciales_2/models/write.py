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


	def write(self, vals):
		res12 = super(SaleOrder, self).write(vals)
		# if self.order_line:
		actualizar_line_origin()
		raise UserError(f'se hizo un cambio en las lineas {lines}')
		return res12



	def actualizar_line_origin(self):
		lines = [(5, 0, 0)]
		self.write({'order_line_origin': lines})
		raise UserError(f'se hizo un cambio en las lineas {self.order_line}')
		for soo in self.order_line:
			ltax = [(5, 0, 0)]
			latax = [(5, 0, 0)]
			
			for tsoo in soo.tax_id:
				ltax[(0, 0, {'id', tsoo.id})]
			
			for atsoo in soo.analytic_tag_ids:
				latax[(0, 0, {'id', atsoo.id})]
			
			lines = [(0, 0, {'order_id': soo.order_id.id,
				'name': soo.name,
				'sequence':soo.sequence,
				'price_unit': soo.price_unit,
				'price_subtotal': soo.price_subtotal,
				'price_tax': soo.price_tax,
				'price_total': soo.price_total,
				'price_reduce': soo.price_reduce,
				# 'tax_id': ltax, # asdfas
				'price_reduce_taxinc': soo.price_reduce_taxinc,
				'price_reduce_taxexcl': soo.price_reduce_taxexcl,
				'discount': soo.discount,
				'product_id': soo.product_id.id,
				# 'product_updatable': soo.product_updatable,
				'product_uom_qty': soo.product_uom_qty,
				'product_uom': soo.product_uom.id,
				'product_uom_category_id': soo.product_uom_category_id.id,
				'product_uom_readonly': soo.product_uom_readonly,
				'salesman_id': soo.salesman_id.id,
				'currency_id': soo.currency_id.id,
				'company_id': soo.company_id.id,
				'order_partner_id': soo.order_partner_id.id,
				# 'qty_delivered_method': soo.qty_delivered_method,
				# 'analytic_tag_ids': latax,
				'is_expense': soo.is_expense,
				'is_downpayment': soo.is_downpayment,
				'customer_lead': soo.customer_lead,
				'display_type': soo.display_type,
				'product_packaging_id': soo.product_packaging_id.id,
				'product_packaging_qty': soo.product_packaging_qty})]
		self.write({'order_line_origin': lines})
	# order_line