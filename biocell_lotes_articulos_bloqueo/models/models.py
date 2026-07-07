# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockProductionLot(models.Model):
	_inherit = 'stock.production.lot'

	can_edit_field = fields.Boolean(string='Puede editar', compute='_compute_can_edit_field_stock_production_lot')

	@api.onchange('company_id')
	def _compute_can_edit_field_stock_production_lot(self):
		for record in self:
			user = self.env.user
			record.can_edit_field = user.has_group('biocell_lotes_articulos_bloqueo.batch_editing_group_it')
