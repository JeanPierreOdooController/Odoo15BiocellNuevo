# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class product_pricelist_item(models.Model):
	_inherit = 'product.pricelist.item'

	code_product = fields.Char(compute="get_codigo", string="Código de Producto", )
	
	def get_codigo(self):
		for i in self:
				i.code_product =  i.product_id.default_code if i.product_id.id else i.product_tmpl_id.default_code