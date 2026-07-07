# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class KardexEntryOutcomeBook(models.Model):
	_inherit = 'kardex.entry.outcome.book'
	
	lot = fields.Char(string=_('Lote'))