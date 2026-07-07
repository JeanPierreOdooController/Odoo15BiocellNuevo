# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date
import json

class Partner(models.Model):
	_inherit = "res.partner"

	type = fields.Selection(
		[('contact', 'Contacto'),
			('invoice', 'Dirección de factura'),
			('delivery', 'Dirección de entrega'),
			('other', 'Otra dirección'),
			("private", "Dirección Privada"),
			("medical_center", "Centro Médico"),
		], string='Address Type',
		default='other',
		help="Invoice & Delivery addresses are used in sales orders. Private addresses are only visible by authorized users.")