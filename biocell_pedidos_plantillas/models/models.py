# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class SaleOrderTemplate(models.Model):
	_inherit = "sale.order.template"

	sale_type = fields.Selection([('sale', "Venta"),('stock', "Inventario")], default=False, help="Seleccione el tipo de venta para poder ubicar la plantilla correctamente.", string=u'Tipo de Venta')
	sale_type_category_id = fields.Many2one('sale.order.category', string=u'Categoría Venta')
	sale_type_id = fields.Many2one('sale.category', string=u'Tipo de Categoría')



# FALTA HACER UN PROCEDIMIENTO QUE CADA QUE SE ELIJA UNA CATEGORIA SE SOBREESCRIBA EL NOMBRE NORMAL


class SaleCategory(models.Model):
	_name = 'sale.category'
	_description = "Tipo de Categorias de ventas"

	name = fields.Char(string=u'Nombre')
	description = fields.Text(string=u'Descripción')
	# sale_order_id = fields.Many2one('sale.order.template', 'Plantilla de Cotizaciòn')



class SaleTypeCategory(models.Model):
	_name = 'sale.order.category'
	_description = "Categorias de ventas"

	name = fields.Char(string=u'Nombre')
	description = fields.Text(string=u'Descripción')
	# sale_order_id = fields.Many2one('sale.order.template', 'Plantilla de Cotizaciòn')

	