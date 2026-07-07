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
	_inherit = "facturacion.venta.pendiente"

	def action_redirect_to_order_it(self):
		sale_order = self.pedido

		if sale_order:
			return {
				'name': 'Sale Order',
				'view_mode': 'form',
				'res_model': 'sale.order',
				'type': 'ir.actions.act_window',
				'res_id': sale_order.id,
				'target': 'current',
			}
