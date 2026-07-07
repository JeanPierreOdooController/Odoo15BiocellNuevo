# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, float_round


class SaleOrderLineOrigin(models.Model):
	_name = 'sale.order.line.origin'
	_description = 'Linea de pedidos original'
	_order = 'order_id, sequence, id'
	_check_company_auto = True


	order_line_id = fields.Many2one('sale.order.line', string="linea de pedido", tracking=1)
	order_id = fields.Many2one('sale.order', string='Pedido de Referencia', required=True, ondelete='cascade', index=True, copy=False)
	name = fields.Text(string='Descripción', required=True)
	sequence = fields.Integer(string='Secuencia', default=10)

	# invoice_lines = fields.Many2many('account.move.line', 'sale_order_line_invoice_rel', 'order_line_id', 'invoice_line_id', string='Invoice Lines', copy=False)
	# invoice_status = fields.Selection([
	#     ('upselling', 'Upselling Opportunity'),
	#     ('invoiced', 'Fully Invoiced'),
	#     ('to invoice', 'To Invoice'),
	#     ('no', 'Nothing to Invoice')
	#     ], string='Invoice Status', compute='_compute_invoice_status', store=True, default='no')
	price_unit = fields.Float('Precio Unitario', required=True, digits='Product Price', default=0.0)

	price_subtotal = fields.Monetary(string='Subtotal', store=True)
	price_tax = fields.Float(string='Total impuestos', store=True)
	price_total = fields.Monetary(string='Total', store=True)

	price_reduce = fields.Float(string='Precio Reducido', digits='Product Price', store=True)
	tax_id = fields.Many2many('account.tax', string='Impuestos', context={'active_test': False})
	price_reduce_taxinc = fields.Monetary(string='Precio Reducir Impuestos Inc.', store=True)
	price_reduce_taxexcl = fields.Monetary(string='Precio Reducir Impuestos excl.', store=True)

	discount = fields.Float(string='Descuento (%)', digits='Discount', default=0.0)

	product_id = fields.Many2one(
		'product.product', string='Producto', domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
		change_default=True, ondelete='restrict', check_company=True)  # Unrequired company
	product_template_id = fields.Many2one(
		'product.template', string='Plantilla de Producto',
		related="product_id.product_tmpl_id", domain=[('sale_ok', '=', True)])
	product_updatable = fields.Boolean(string='Puede editar el producto', default=True)
	product_uom_qty = fields.Float(string='Cantidad', digits='Product Unit of Measure', required=True, default=1.0)
	product_uom = fields.Many2one('uom.uom', string='Unidad de medida', domain="[('category_id', '=', product_uom_category_id)]", ondelete="restrict")
	product_uom_category_id = fields.Char()
	product_uom_readonly = fields.Boolean()
	product_custom_attribute_value_ids = fields.One2many('product.attribute.custom.value', 'sale_order_line_id', string="Valores personalizados", copy=True)


	product_no_variant_attribute_value_ids = fields.Many2many('product.template.attribute.value', string="Valores adicionales", ondelete='restrict')

	qty_delivered = fields.Float('Cantidad entregada', copy=False, digits='Product Unit of Measure', default=0.0)
	qty_delivered_manual = fields.Float('Entregado manualmente', copy=False, digits='Product Unit of Measure', default=0.0)

	# qty_delivered_method = fields.Selection([
	# 	('manual', 'Manual'),
	# 	('analytic', 'Analytic From Expenses')
	# ], string="Method to update delivered qty",
	# 	help="According to product configuration, the delivered quantity can be automatically computed by mechanism :\n"
	# 		 "  - Manual: the quantity is set manually on the line\n"
	# 		 "  - Analytic From expenses: the quantity is the quantity sum from posted expenses\n"
	# 		 "  - Timesheet: the quantity is the sum of hours recorded on tasks linked to this sale line\n"
	# 		 "  - Stock Moves: the quantity comes from confirmed pickings\n")
	# qty_to_invoice = fields.Float(
	#     compute='_get_to_invoice_qty', string='To Invoice Quantity', store=True,
	#     digits='Product Unit of Measure')
	# qty_invoiced = fields.Float(
	#     compute='_compute_qty_invoiced', string='Invoiced Quantity', store=True,
	#     digits='Product Unit of Measure')

	# untaxed_amount_invoiced = fields.Monetary("Untaxed Invoiced Amount", compute='_compute_untaxed_amount_invoiced', store=True)
	# untaxed_amount_to_invoice = fields.Monetary("Untaxed Amount To Invoice", compute='_compute_untaxed_amount_to_invoice', store=True)

	salesman_id = fields.Many2one(related='order_id.user_id', store=True, string='Vendedor')
	currency_id = fields.Many2one(related='order_id.currency_id', depends=['order_id.currency_id'], store=True, string='Divisa')
	company_id = fields.Many2one(related='order_id.company_id', string='Compañía', store=True,index=True)
	order_partner_id = fields.Many2one(related='order_id.partner_id', store=True, string='Cliente', index=True)
	analytic_tag_ids = fields.Many2many(
		'account.analytic.tag', string='Etiquetas analíticas', store=True, readonly=False,
		domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
	analytic_line_ids = fields.One2many('account.analytic.line', 'so_line', string="Líneas analíticas")
	is_expense = fields.Boolean('Es gasto', help="Es cierto si la línea de orden de venta proviene de un gasto o de facturas de proveedor.")
	is_downpayment = fields.Boolean(
		string="Es un pago inicial", help="Los pagos iniciales se realizan al crear facturas a partir de un pedido de venta."
		" Ellos no se copian al duplicar un pedido de ventas.")

	state = fields.Selection(
		related='order_id.state', string='Estado del pedido', copy=False, store=True)

	customer_lead = fields.Float(
		'Tiempo de espera', required=True, default=0.0,
		help="Número de días entre la confirmación del pedido y el envío de los productos al cliente")

	display_type = fields.Selection([
		('line_section', "Section"),
		('line_note', "Note")], default=False, help="Technical field for UX purpose.")

	product_packaging_id = fields.Char(string='Embalaje', default=False, domain="[('sales', '=', True), ('product_id','=',product_id)]")
	# product_packaging_id = fields.Many2one('product.packaging', string='Packaging', default=False, domain="[('sales', '=', True), ('product_id','=',product_id)]", check_company=True)
	product_packaging_qty = fields.Float('Cantidad de Embalaje')

	sale_order_template_id = fields.Many2one('sale.order.template',string=u'Pantilla presupuesto')

# class ProductAttributeCustomValue(models.Model):
# 	_inherit = "product.attribute.custom.value"

# 	sale_order_line_id_2 = fields.Many2one('sale.order.line.origin', string="Sales Order Line", required=True, ondelete='cascade')