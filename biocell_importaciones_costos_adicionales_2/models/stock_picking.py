# -*- coding:utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

class StockPicking(models.Model):
	_inherit = 'stock.picking'

	landed_units_id = fields.Many2one('landed.units.specific',string='Gasto Vinculado')