# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.addons.fleet.models.fleet_vehicle_model import FUEL_TYPES

class FleetVehicle(models.Model):
	_inherit = 'fleet.vehicle'


	vehi_default = fields.Boolean(string='Vehículo por defecto')

	@api.constrains('vehi_default')
	def _check_unique_default_vehicle_it(self):
		for record in self:
			if record.vehi_default == True:
				existing_default = self.search([('vehi_default', '=', True), ('id', '!=', record.id)], limit=1)
				if existing_default:
					raise ValidationError("Ya existe un vehículo por defecto. No puedes marcar otro como por defecto.")

class LogisticDespatch(models.Model):
	_inherit = 'logistic.despatch'

	def default_get(self, fields):
		defaults = super(LogisticDespatch, self).default_get(fields)
		
		if 'vehicle_id' in fields and not defaults.get('vehicle_id'):
			seb = self.env['fleet.vehicle'].sudo().search([('vehi_default', '=', True)], limit=1)
			if seb:
				defaults['vehicle_id'] = seb.id
				defaults['driver_id'] = seb.driver_id.id

		return defaults


	# @api.onchange('vehicle_id')
	# def _onchange_vehicle_id_it(self):
	# 	for di in self:
	# 		if not di.vehicle_id:
	# 			seb = self.env['fleet.vehicle'].sudo().search([('vehi_default','=',True)], limit=1)
	# 			if seb:
	# 				di.vehicle_id = seb.id
	# 				di.driver_id = seb.driver_id.id
