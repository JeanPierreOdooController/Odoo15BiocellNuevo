# -*- coding:utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

class AccountMove(models.Model):
	_inherit = 'account.move'

	landed_cost_units_id = fields.Many2one('landed.units.specific',string='Gasto Vinculado')