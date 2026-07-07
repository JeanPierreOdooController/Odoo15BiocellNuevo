# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date
import json

class SaleOrder(models.Model):
	_inherit = 'sale.order'
	"""
		2/19/24
		Se agrego Tracking al campo de Fecha/Hora Cirugia
 	"""
	sugery_date = fields.Datetime(
    	string=u'Fecha/Hora Cirugía',
		tracking=True
    )
 
	@api.onchange('pricelist_id')
	def onchange_pricelist_id_it(self):
		if self.pricelist_id:
			# raise ('ingreso')
			sale_orders = self.env['sale.order'].sudo().search([('name','=',self.name)])
			for sale_order in sale_orders:
				sale_order_lines = self.env['sale.order.line'].sudo().search([
					('order_id','=',sale_order.id)
				])
				for sale_order_line in sale_order_lines:
					price_unit_it = 0.0
					discount_it = 0.0
					if not sale_order_line.product_id:
						# Si la línea de pedido no tiene un producto asignado, evita la modificación
						continue
					existe = self.env['product.pricelist.item'].sudo().search([
						("applied_on","=","3_global"),
						('pricelist_id','=',self.pricelist_id.id),
						('compute_price','=','percentage'),
					], limit=1)
					if existe:
						if self.pricelist_id.discount_policy == 'without_discount':
							price_unit_it = sale_order_line.product_id.list_price
							discount_it = existe.percent_price
						else:
							price_unit_it = sale_order_line.product_id.list_price-(existe.percent_price*0.01)*sale_order_line.product_id.list_price
					else:
						existe = self.env['product.pricelist.item'].sudo().search([
							("applied_on","=","3_global"),
							('pricelist_id','=',self.pricelist_id.id),
							('compute_price','=','fixed'),
						], limit=1)
						if existe:
							price_unit_it = existe.fixed_price
						else:
							existe = self.env["product.pricelist.item"].sudo().search([
								("product_tmpl_id","=",sale_order_line.product_id.product_tmpl_id.id),
								('pricelist_id','=',self.pricelist_id.id)
							], limit=1)
							if not existe:
								existe = self.env["product.pricelist.item"].sudo().search([
									("product_id","=",sale_order_line.product_id.id),
									('pricelist_id','=',self.pricelist_id.id)
								], limit=1)
							if existe:
								price_unit_it = existe.fixed_price
							else:
								price_unit_it = sale_order_line.product_id.list_price
					
					# Actualizar el precio solo si la línea es editable
					if sale_order_line.display_type != 'line_section':
						sale_order_line.price_unit = price_unit_it
						sale_order_line.sudo().write({'price_unit': price_unit_it})
						if self.pricelist_id.discount_policy == 'without_discount':
							sale_order_line.sudo().write({'discount': discount_it})
						else:
							sale_order_line.sudo().write({'discount': discount_it})


	@api.onchange('plantilla_presupuesto_id')
	def onchange_plantilla_presupuesto_id(self):
		if self.plantilla_presupuesto_id.ids:
			plantillas_existen = []
			plantillas_faltan = []
			lineas_a_eliminar = []
			for i in self.order_line.filtered(lambda r: r.sale_type == 'sale'):
				if i.sale_order_template_id.id and i.sale_order_template_id.id in self.plantilla_presupuesto_id.ids:
					plantillas_existen.append(i.sale_order_template_id.id)
				elif i.sale_order_template_id.id:
					lineas_a_eliminar.append((3, i.id, 0))  # Marcamos las líneas para eliminar

				else:
					pass
			if lineas_a_eliminar != []:
				self.order_line = lineas_a_eliminar  # Eliminar líneas marcadas
			plantillas_faltan = list( set(self.plantilla_presupuesto_id.ids) - set(plantillas_existen) )
			nuevadata = []
			for i in plantillas_faltan:
				plantilla_obj = self.env['sale.order.template'].browse(i)
				nuevadata.append( (0,0, {
						'display_type': 'line_section',
						'name': plantilla_obj.name,
						'sale_order_template_id': i,
						'sale_type':'sale',
					}) )
				for det in plantilla_obj.sale_order_template_line_ids:
					price_unit_it = 0.0
					discount_it = 0.0
					existe = self.env['product.pricelist.item'].sudo().search([("applied_on","=","3_global"),('pricelist_id','=',self.pricelist_id.id,),('compute_price','=','percentage'),], limit=1)
					if existe:
						if self.pricelist_id.discount_policy == 'without_discount':
							price_unit_it = det.product_id.list_price
							discount_it = existe.percent_price
						else:
							price_unit_it = det.product_id.list_price-(existe.percent_price*0.01)*det.product_id.list_price
					else:
						existe = self.env['product.pricelist.item'].sudo().search([("applied_on","=","3_global"),('pricelist_id','=',self.pricelist_id.id),('compute_price','=','fixed'),], limit=1)
						if existe:
							price_unit_it = existe.fixed_price
						else:
							existe = self.env["product.pricelist.item"].sudo().search([("product_tmpl_id","=",det.product_id.product_tmpl_id.id),('pricelist_id','=',self.pricelist_id.id)],limit=1)
							if not existe:
								existe = self.env["product.pricelist.item"].sudo().search([("product_id","=",det.product_id.id),('pricelist_id','=',self.pricelist_id.id)],limit=1)
							if existe:
								price_unit_it = existe.fixed_price
							else:
								price_unit_it = det.product_id.list_price
					nuevadata.append( (0,0, {
							'product_id':det.product_id.id,
							'name':det.name,
							'product_uom_qty':det.product_uom_qty,
							'product_uom': det.product_uom_id.id,
							'sale_order_template_id': i,
							'price_unit': price_unit_it,
							'discount': discount_it,
							'sale_type':'sale',
							'tax_id': [(6,0,det.product_id.taxes_id.filtered(lambda r: r.company_id.id == self.env.company.id).ids)],
					} ) )
			self.order_line = [(4,0)] + nuevadata
		else:
			lineas_a_eliminar = []
			for i in self.order_line.filtered(lambda r: r.sale_type == 'sale'):
				if i.sale_order_template_id.id:
					lineas_a_eliminar.append((3, i.id, 0))  # Marcamos las líneas para eliminar
			if lineas_a_eliminar != []:
				self.order_line = lineas_a_eliminar  # Eliminar líneas marcadas
	

	@api.onchange('plantilla_kardex_id')
	def onchange_plantilla_kardex_id(self):
		if self.plantilla_kardex_id.ids:
			plantillas_existen = []
			plantillas_faltan = []
			lineas_a_eliminar = []
			for i in self.order_line_stock.filtered(lambda r: r.sale_type == 'stock'):
				if i.sale_order_template_id.id and i.sale_order_template_id.id in self.plantilla_kardex_id.ids:
					plantillas_existen.append(i.sale_order_template_id.id)
				elif i.sale_order_template_id.id:
					lineas_a_eliminar.append((3, i.id, 0))  # Marcamos las líneas para eliminar

				else:
					pass
			if lineas_a_eliminar != []:
				self.order_line_stock = lineas_a_eliminar  # Eliminar líneas marcadas
			plantillas_faltan = list( set(self.plantilla_kardex_id.ids) - set(plantillas_existen) )
			nuevadata = []
			for i in plantillas_faltan:
				plantilla_obj = self.env['sale.order.template'].browse(i)
				nuevadata.append( (0,0, {
						'company_id':self.env.company.id,
						'display_type': 'line_section',
						'name': plantilla_obj.name,
						'sale_order_template_id': i,
						'sale_type':'stock',
						
					}) )
				for det in plantilla_obj.sale_order_template_line_ids:
					price_unit_it = 0.0
					discount_it = 0.0
					existe = self.env['product.pricelist.item'].sudo().search([("applied_on","=","3_global"),('pricelist_id','=',self.pricelist_id.id),('compute_price','=','percentage'),], limit=1)
					if existe:
						if self.pricelist_id.discount_policy == 'without_discount':
							price_unit_it = det.product_id.list_price
							discount_it = existe.percent_price
						else:
							price_unit_it = det.product_id.list_price-(existe.percent_price*0.01)*det.product_id.list_price
					else:
						existe = self.env['product.pricelist.item'].sudo().search([("applied_on","=","3_global"),('pricelist_id','=',self.pricelist_id.id),('compute_price','=','fixed'),], limit=1)
						if existe:
							price_unit_it = existe.fixed_price
						else:
							existe = self.env["product.pricelist.item"].sudo().search([("product_tmpl_id","=",det.product_id.product_tmpl_id.id),('pricelist_id','=',self.pricelist_id.id)],limit=1)
							if not existe:
								existe = self.env["product.pricelist.item"].sudo().search([("product_id","=",det.product_id.id),('pricelist_id','=',self.pricelist_id.id)],limit=1)
							if existe:
								price_unit_it = existe.fixed_price
							else:
								price_unit_it = det.product_id.list_price
					nuevadata.append( (0,0, {
							'company_id':self.env.company.id,
							'product_id':det.product_id.id,
							'name':det.name,
							'product_uom_qty':det.product_uom_qty,
							'product_uom': det.product_uom_id.id,
							'sale_order_template_id': i,
							'price_unit': price_unit_it,
							'discount': discount_it,
							'sale_type':'stock',
							'tax_id': [(6,0,det.product_id.taxes_id.filtered(lambda r: r.company_id.id == self.env.company.id).ids)],
					} ) )
			self.order_line_stock = [(4,0)] + nuevadata
		else:
			lineas_a_eliminar = []
			for i in self.order_line_stock.filtered(lambda r: r.sale_type == 'stock'):
				if i.sale_order_template_id.id:
					lineas_a_eliminar.append((3, i.id, 0))  # Marcamos las líneas para eliminar
			if lineas_a_eliminar != []:
				self.order_line_stock = lineas_a_eliminar  # Eliminar líneas marcadas


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'


	@api.onchange('product_id')
	def product_id_it_new(self):
		if self.product_id:
			price_unit_it = 0.0
			discount_it = 0.0
			if self.sale_type == 'sale':
				# raise UserError('test')
				existe = self.env['product.pricelist.item'].sudo().search([("applied_on","=","3_global"),('pricelist_id','=',self.order_id.pricelist_id.id),('compute_price','=','percentage'),], limit=1)
				if existe:
					if self.order_id.pricelist_id.discount_policy == 'without_discount':
						discount_it = existe.percent_price
						price_unit_it = self.product_id.list_price
					else:
						price_unit_it = self.product_id.list_price-(existe.percent_price*0.01)*self.product_id.list_price
				else:
					existe = self.env['product.pricelist.item'].sudo().search([("applied_on","=","3_global"),('pricelist_id','=',self.order_id.pricelist_id.id),('compute_price','=','fixed'),], limit=1)
					if existe:
						price_unit_it = existe.fixed_price
					else:			
						existe_2 = self.env["product.pricelist.item"].sudo().search([("product_tmpl_id","=",self.product_id.product_tmpl_id.id),('pricelist_id','=',self.order_id.pricelist_id.id)],limit=1)
						if not existe_2:
							existe_2 = self.env["product.pricelist.item"].sudo().search([("product_id","=",self.product_id.id),('pricelist_id','=',self.order_id.pricelist_id.id)],limit=1)
						if existe_2:
							price_unit_it = existe_2.fixed_price
						else:
							price_unit_it = self.product_id.list_price
			if self.sale_type == 'stock':
				# raise UserError('test')
				existe = self.env['product.pricelist.item'].sudo().search([("applied_on","=","3_global"),('pricelist_id','=',self.order_id_stock.pricelist_id.id),('compute_price','=','percentage'),], limit=1)
				if existe:
					if self.order_id_stock.pricelist_id.discount_policy == 'without_discount':
						discount_it = existe.percent_price
						price_unit_it = self.product_id.list_price
					else:
						price_unit_it = self.product_id.list_price-(existe.percent_price*0.01)*self.product_id.list_price
				else:
					existe = self.env['product.pricelist.item'].sudo().search([("applied_on","=","3_global"),('pricelist_id','=',self.order_id_stock.pricelist_id.id),('compute_price','=','fixed'),], limit=1)
					if existe:
						price_unit_it = existe.fixed_price
					else:			
						existe_2 = self.env["product.pricelist.item"].sudo().search([("product_tmpl_id","=",self.product_id.product_tmpl_id.id),('pricelist_id','=',self.order_id_stock.pricelist_id.id)],limit=1)
						if not existe_2:
							existe_2 = self.env["product.pricelist.item"].sudo().search([("product_id","=",self.product_id.id),('pricelist_id','=',self.order_id_stock.pricelist_id.id)],limit=1)
						if existe_2:
							price_unit_it = existe_2.fixed_price
						else:
							price_unit_it = self.product_id.list_price
				# raise UserError('test')
			
			self.discount = discount_it
			self.price_unit = price_unit_it