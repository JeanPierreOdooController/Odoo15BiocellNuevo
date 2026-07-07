# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

class AccountMoveLine(models.Model):
	_inherit = 'account.move.line'
	
	invoice_date_landed_units = fields.Date(related='move_id.invoice_date',string='Fecha Factura')
	is_landed_units = fields.Boolean(related='product_id.product_tmpl_id.is_landed_cost',string='Usa GV')
	landed_units_id = fields.Many2one('landed.units.specific',related='move_id.landed_cost_units_id',string='Gasto Vinculado',store=True)