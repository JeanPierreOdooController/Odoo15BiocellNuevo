# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date
import json

class ResPartner(models.Model):
	_inherit = 'res.partner'

	is_medic = fields.Boolean(default=False, string=u'Es Médico')
	cmp = fields.Char(string=u'CMP')
	is_instrumentalist = fields.Boolean(default=False, string=u'Es Instrumentista')
	