# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import UserError
from odoo.tools.misc import formatLang, format_date, get_lang

class AccountBalancePeriodBook(models.Model):
	_inherit = 'account.balance.period.book'
	
	invoice_internal = fields.Boolean(string=('Factura Internada'), default=False)
	date_invoice_internal = fields.Date(
		string=('Fecha de Factura Interna'),
	)
