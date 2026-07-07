# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date

class SaleCategory(models.Model):
	_name = 'sale.category'

	name = fields.Char(string='Nombre', required= True)
	description = fields.Text(string=u'Descripción')