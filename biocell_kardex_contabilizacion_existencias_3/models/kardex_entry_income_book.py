# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class KardexEntryIncomeBook(models.Model):
	_inherit = 'kardex.entry.income.book'
	
	lot = fields.Char(string=_('Lote'))