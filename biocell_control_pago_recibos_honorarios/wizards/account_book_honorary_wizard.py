# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import *
from odoo.exceptions import UserError
import base64

from io import BytesIO
import re
import uuid

class AccountBookHonoraryWizard(models.TransientModel):
	_inherit = 'account.book.honorary.wizard'

	type_date = fields.Selection(selection_add=[
        ('payment_date','Fecha de Pago')
    ], ondelete={'payment_date': 'cascade'})