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
	tax_totals_json_origin = fields.Char(compute='_compute_tax_totals_json_origin')
	note_origin = fields.Text(string=u'Nota')
	amount_untaxed_origin = fields.Monetary(string='Untaxed Amount', store=True, compute='_amount_all2', tracking=5)
	amount_tax_origin = fields.Monetary(string='Taxes', store=True, compute='_amount_all2')
	amount_total_origin = fields.Monetary(string='Total', store=True, compute='_amount_all2', tracking=4)
	order_line_origin = fields.One2many('sale.order.line.origin', 'order_id', string='Lineas de pedido Originales', copy=True)
	
	@api.depends('order_line_origin.tax_id', 'order_line_origin.price_unit', 'amount_total_origin', 'amount_untaxed_origin')
	def _compute_tax_totals_json_origin(self):
		def compute_taxes_2(order_line_origin):
			price = order_line_origin.price_unit * (1 - (order_line_origin.discount or 0.0) / 100.0)
			order = order_line_origin.order_id
			return order_line_origin.tax_id._origin.compute_all(price, order.currency_id, order_line_origin.product_uom_qty, product=order_line_origin.product_id, partner=order.partner_shipping_id)

		account_move = self.env['account.move']
		for order in self:
			tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line_origin, compute_taxes_2)
			tax_totals = account_move._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total_origin, order.amount_untaxed_origin, order.currency_id)
			order.tax_totals_json_origin = json.dumps(tax_totals)


	@api.depends('order_line_origin.price_total')
	def _amount_all2(self):
		"""
		Compute the total amounts of the SO.
		"""
		for order in self:
			amount_untaxed_origin = amount_tax_origin = 0.0
			for line in order.order_line_origin:
				amount_untaxed_origin += line.price_subtotal
				amount_tax_origin += line.price_tax
			order.update({
				'amount_untaxed_origin': amount_untaxed_origin,
				'amount_tax_origin': amount_tax_origin,
				'amount_total_origin': amount_untaxed_origin + amount_tax_origin,
			})


