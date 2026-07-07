# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	plantilla_presupuesto_id = fields.Many2many('sale.order.template',string=u'Plantilla de presupuesto')
	plantilla_kardex_id = fields.Many2many('sale.order.template',string=u'Plantilla de Kardex')
