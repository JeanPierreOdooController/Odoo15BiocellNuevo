# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountBookDiaryView(models.Model):
	_inherit = 'account.book.diary.view'
	
	employee_id = fields.Many2one('hr.employee', string='Empleado',copy=False)