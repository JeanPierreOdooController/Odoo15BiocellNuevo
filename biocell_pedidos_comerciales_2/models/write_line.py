# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, float_round


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	package_id = fields.Many2one('stock.quant.package','Paquete')
	confirm_it = fields.Boolean(default=False)
	line_venta_it = fields.Boolean()
	
	@api.model
	def create(self, vals):
		request = super(SaleOrderLine, self).create(vals)
		otros = request.order_id.order_line.filtered(lambda r: r.package_id.id) 
		if len(otros)!= 0:
			return request
		# raise UserError('ingreso')
		for res in request:
			if request.sale_type != "stock":
				line_date = request.create_date
				order_date = request.order_id.create_date
				diff_seconds = abs((line_date - order_date).total_seconds())
				if request.confirm_it == False and diff_seconds <= 1:
					for soo in request:
						# raise UserError('ingreso')
						order_line_origin = self.env['sale.order.line.origin'].sudo().create({
							'order_line_id': request.id,
							'order_id': request.order_id.id,
							'name': request.name,
							'sequence':request.sequence,
							'price_unit': request.price_unit,
							'price_subtotal': request.price_subtotal,
							'price_tax': request.price_tax,
							'price_total': request.price_total,
							'price_reduce': request.price_reduce,
							'tax_id': request.tax_id, # asdfas
							'price_reduce_taxinc': request.price_reduce_taxinc,
							'price_reduce_taxexcl': request.price_reduce_taxexcl,
							'discount': request.discount,
							'product_id': request.product_id.id,
							# 'product_updatable': request.product_updatable,
							'product_uom_qty': request.product_uom_qty,
							'product_uom': request.product_uom.id,
							'product_uom_category_id': request.product_uom_category_id.id,
							'product_uom_readonly': request.product_uom_readonly,
							# 'salesman_id': request.salesman_id.id,
							# 'currency_id': request.currency_id.id,
							# 'company_id': request.company_id.id,
							# 'order_partner_id': request.order_partner_id.id,
							# 'qty_delivered_method': request.qty_delivered_method,
							'analytic_tag_ids': request.analytic_tag_ids,
							'is_expense': request.is_expense,
							'is_downpayment': request.is_downpayment,
							'customer_lead': request.customer_lead,
							'display_type': request.display_type,
							'product_packaging_id': request.product_packaging_id.id,
							'product_packaging_qty': request.product_packaging_qty,
							# 'state_old_confirm': '01',
							# 'confirm_old_id': request.id,
							'sale_order_template_id': request.sale_order_template_id.id
						})
		return request


	"""
	def write(selfs, vals):
		res12 = super(SaleOrderLine, selfs).write(vals)		
		otros = selfs[0].order_id.order_line.filtered(lambda r: r.package_id.id) 
		if len(otros)!= 0:
			return res12
		for self in selfs:
			if self.sale_type != "stock":
				if self.confirm_it == False:
					soo_old = self.env['sale.order.line.origin'].sudo().search([('order_line_id','=',self.id)])
					soo_old.sudo().write({
							'order_id': self.order_id.id,
							'name': self.name,
							'sequence':self.sequence,
							'price_unit': self.price_unit,
							'price_subtotal': self.price_subtotal,
							'price_tax': self.price_tax,
							'price_total': self.price_total,
							'price_reduce': self.price_reduce,
							'tax_id': self.tax_id, # asdfas
							'price_reduce_taxinc': self.price_reduce_taxinc,
							'price_reduce_taxexcl': self.price_reduce_taxexcl,
							'discount': self.discount,
							'product_id': self.product_id.id,
							# 'product_updatable': self.product_updatable,
							'product_uom_qty': self.product_uom_qty,
							'product_uom': self.product_uom.id,
							'product_uom_category_id': self.product_uom_category_id.id,
							'product_uom_readonly': self.product_uom_readonly,
							# 'salesman_id': self.salesman_id.id,
							# 'currency_id': self.currency_id.id,
							# 'company_id': self.company_id.id,
							# 'order_partner_id': self.order_partner_id.id,
							# 'qty_delivered_method': self.qty_delivered_method,
							'analytic_tag_ids': self.analytic_tag_ids,
							'is_expense': self.is_expense,
							'is_downpayment': self.is_downpayment,
							'customer_lead': self.customer_lead,
							'display_type': self.display_type,
							'product_packaging_id': self.product_packaging_id.id,
							'product_packaging_qty': self.product_packaging_qty,
							# 'confirm_old_id': self.id,
							# 'state_old_confirm': '01',
							'sale_order_template_id': self.sale_order_template_id.id
						})
		return res12"""




	def unlink(self):
		for record in self:
			if record.sale_type != "stock":							
				otros = record.order_id.order_line.filtered(lambda r: r.package_id.id) 
				if len(otros)== 0 and record.confirm_it == False:
					soo_old2 = self.env['sale.order.line.origin'].sudo().search([('order_line_id','=',record.id)])
					soo_old2.unlink() 
		soo2_old = super(SaleOrderLine, self).unlink()
		return soo2_old
