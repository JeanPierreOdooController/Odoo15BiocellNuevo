# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import tools


class sale_order(models.Model):
	_inherit = 'sale.order'

	aprob_id  = fields.Boolean(u'Aprobado',default=False)
	desaprob_id  = fields.Boolean(u'Desaprobado',default=False)

	@api.model
	def create(self, vals):
		c = super(sale_order, self).create(vals)
		c.aprob_id = False
		c.desaprob_id = False
		return c


	def aprobarhc(self):
		a = super(sale_order,self).aprobarhc()
		self.aprob_id = True
		return a


	def desaprobarhc(self):
		b = super(sale_order,self).desaprobarhc()
		self.aprob_id = False
		self.desaprob_id = True
		return b