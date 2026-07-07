# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date
import json

class procedure_clinic(models.Model):
	_name = 'procedure.clinic'

	procedure_id = fields.Char(string=u'Código')
	name = fields.Char(string=u'Nombre de Procedimiento Clínico')