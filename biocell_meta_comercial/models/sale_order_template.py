# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date
import json

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	plantilla_presupuesto_id = fields.Many2many('sale.order.template','sale_order_sale_order_template_rel','order_id','template_id',string=u'Plantilla de presupuesto',
		readonly=True, check_company=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
		domain=[('sale_type','=','sale')])
	
	plantilla_kardex_id = fields.Many2many('sale.order.template','sale_order_sale_order_template_rel_kardex','order_id','template_id',string=u'Plantilla de Kardex',
		readonly=True, check_company=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain=[('sale_type','=','stock')])
	
	order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True, domain=[('sale_type','=','sale')])
	order_line_stock = fields.One2many('sale.order.line', 'order_id_stock', string='Order Lines Stock', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True, domain=[('sale_type','=','stock')])

	name_patient = fields.Char(string=u'Nombre Paciente',required=True)
	patient_vat = fields.Char(string = u'Paciente DNI/RUC')
	clinic_history = fields.Char(string= u'Historial Clínico')
	medic_center = fields.Many2one('res.partner', string='Centro Médico',required=True)
	name_doctor = fields.Many2one('res.partner',string=u'Nombre del Doctor',required=True)
	sugery_date = fields.Datetime(string=u'Fecha/Hora Cirugía')
	sugery_order = fields.Char(string=u'Orden de Cirugía')
	procedure_clinic = fields.Char(string=u'Procedimiento Clínico',required=False)
	procedure_clinic_id = fields.Many2one('procedure.clinic', string=u'Procedimiento Clínico',required=True)
	instrumentalist = fields.Many2one('res.partner',string=u'Instrumentista')

	request_date = fields.Datetime(string=u'Fecha de Solicitud de Cotización')
	schedulling_request_date = fields.Datetime(string=u'Fecha de Solicitud de Agendamiento')

	descuento_masivo = fields.Float('Descuento')


	
	tax_totals_json_kardex = fields.Char(compute='_compute_tax_totals_json_kardex')
	note_kardex = fields.Text(string=u'Nota')
	amount_untaxed_kardex = fields.Monetary(string='Untaxed Amount', store=True, compute='_amount_all3', tracking=5)
	amount_tax_kardex= fields.Monetary(string='Taxes', store=True, compute='_amount_all3')
	amount_total_kardex = fields.Monetary(string='Total', store=True, compute='_amount_all3', tracking=4)
	


	validity_term = fields.Many2one('account.payment.term', string=u"Términos de Validez")
	shop_id = fields.Many2one('account.analytic.journal', string=u'Centro')
	carrier_id = fields.Char( string=u'no sirve')


	warehouse_id = fields.Many2one('stock.warehouse', string=u"Almacén")

	def aplicar_descuento(self):
		for i in self:
			i.order_line.write({'discount': self.descuento_masivo})
			i.order_line_stock.write({'discount': self.descuento_masivo})
			i.order_line._compute_amount()
			i.order_line_stock._compute_amount()
	

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
					nuevadata.append( (0,0, {
							'product_id':det.product_id.id,
							'name':det.name,
							'product_uom_qty':det.product_uom_qty,
							'product_uom': det.product_uom_id.id,
							'sale_order_template_id': i,
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
					nuevadata.append( (0,0, {
							'company_id':self.env.company.id,
							'product_id':det.product_id.id,
							'name':det.name,
							'product_uom_qty':det.product_uom_qty,
							'product_uom': det.product_uom_id.id,
							'sale_order_template_id': i,
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
	

	@api.depends('order_line_stock.tax_id', 'order_line_stock.price_unit', 'amount_total_kardex', 'amount_untaxed_kardex')
	def _compute_tax_totals_json_kardex(self):
		def compute_taxes_2(order_line_stock):
			price = order_line_stock.price_unit * (1 - (order_line_stock.discount or 0.0) / 100.0)
			order = order_line_stock.order_id
			return order_line_stock.tax_id.filtered(lambda r: r.company_id.id == self.env.company.id)._origin.compute_all(price, order.currency_id, order_line_stock.product_uom_qty, product=order_line_stock.product_id, partner=order.partner_shipping_id)

		account_move = self.env['account.move']
		for order in self:
			tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line_stock, compute_taxes_2)
			tax_totals = account_move._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total_kardex, order.amount_untaxed_kardex, order.currency_id)
			order.tax_totals_json_kardex = json.dumps(tax_totals)


	@api.depends('order_line_stock.price_total')
	def _amount_all3(self):
		"""
		Compute the total amounts of the SO.
		"""
		for order in self:
			amount_untaxed_kardex = amount_tax_kardex = 0.0
			for line in order.order_line_stock:
				amount_untaxed_kardex += line.price_subtotal
				amount_tax_kardex += line.price_tax
			order.update({
				'amount_untaxed_kardex': amount_untaxed_kardex,
				'amount_tax_kardex': amount_tax_kardex,
				'amount_total_kardex': amount_untaxed_kardex + amount_tax_kardex,
			})

	def _get_update_prices_lines(self):
		return self.order_line_stock.filtered(lambda line: not line.display_type) + self.order_line.filtered(lambda line: not line.display_type)


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'
	order_id = fields.Many2one(required=False)
	sale_order_template_id = fields.Many2one('sale.order.template',string=u'Pantilla presupuesto')
	sale_type = fields.Selection([('sale', 'VENTA'),('stock', 'INVENTARIO')], string=u"tipo venta")
	order_id_stock = fields.Many2one('sale.order', string='Order Reference Stock', required=False, ondelete='cascade', index=True, copy=False)
	company_id = fields.Many2one( 'res.company', related= False,compute='compute_company_id', string='Company', store=True, index=True)

	@api.depends('order_id','order_id_stock')
	def compute_company_id(self):
		for i in self:
			i.company_id = i.order_id.company_id.id if i.order_id.id else i.order_id_stock.company_id.id 
	
	@api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id')
	def _onchange_discount(self):
		if not (self.product_id and self.product_uom and
				(self.order_id.partner_id or self.order_id_stock.partner_id ) and (self.order_id.pricelist_id or self.order_id_stock.pricelist_id) and
				(self.order_id.pricelist_id.discount_policy == 'without_discount' or self.order_id_stock.pricelist_id.discount_policy == 'without_discount') and
				self.env.user.has_group('product.group_discount_per_so_line')):
			return

		self.discount = 0.0
		product = self.product_id.with_context(
			lang=self.order_id.partner_id.lang or self.order_id_stock.partner_id.lang ,
			partner=self.order_id.partner_id or self.order_id_stock.partner_id,
			quantity=self.product_uom_qty,
			date=self.order_id.date_order or self.order_id_stock.date_order,
			pricelist=self.order_id.pricelist_id.id or self.order_id_stock.pricelist_id.id,
			uom=self.product_uom.id,
			fiscal_position=self.env.context.get('fiscal_position')
		)

		product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id or self.order_id_stock.partner_id.id, date=self.order_id.date_order or self.order_id_stock.date_order, uom=self.product_uom.id)

		if self.order_id.id:
			price, rule_id = self.order_id.pricelist_id.with_context(product_context).get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
			new_list_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, self.order_id.pricelist_id.id)

			if new_list_price != 0:
				if self.order_id.pricelist_id.currency_id != currency:
					# we need new_list_price in the same currency as price, which is in the SO's pricelist's currency
					new_list_price = currency._convert(
						new_list_price, self.order_id.pricelist_id.currency_id,
						self.order_id.company_id or self.env.company, self.order_id.date_order or fields.Date.today())
				discount = (new_list_price - price) / new_list_price * 100
				if (discount > 0 and new_list_price > 0) or (discount < 0 and new_list_price < 0):
					self.discount = discount
		if self.order_id_stock.id :
			price, rule_id = self.order_id_stock.pricelist_id.with_context(product_context).get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id_stock.partner_id)
			new_list_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, self.order_id_stock.pricelist_id.id)

			if new_list_price != 0:
				if self.order_id_stock.pricelist_id.currency_id != currency:
					# we need new_list_price in the same currency as price, which is in the SO's pricelist's currency
					new_list_price = currency._convert(
						new_list_price, self.order_id_stock.pricelist_id.currency_id,
						self.order_id_stock.company_id or self.env.company, self.order_id_stock.date_order or fields.Date.today())
				discount = (new_list_price - price) / new_list_price * 100
				if (discount > 0 and new_list_price > 0) or (discount < 0 and new_list_price < 0):
					self.discount = discount

	@api.onchange('product_uom', 'product_uom_qty')
	def product_uom_change(self):
		if self.order_id.id:
			if not self.product_uom or not self.product_id:
				self.price_unit = 0.0
				return
			if self.order_id.pricelist_id and self.order_id.partner_id:
				product = self.product_id.with_context(
					lang=self.order_id.partner_id.lang,
					partner=self.order_id.partner_id,
					quantity=self.product_uom_qty,
					date=self.order_id.date_order,
					pricelist=self.order_id.pricelist_id.id,
					uom=self.product_uom.id,
					fiscal_position=self.env.context.get('fiscal_position')
				)
				self.price_unit = product._get_tax_included_unit_price(
					self.company_id or self.order_id.company_id,
					self.order_id.currency_id,
					self.order_id.date_order,
					'sale',
					fiscal_position=self.order_id.fiscal_position_id,
					product_price_unit=self._get_display_price(product),
					product_currency=self.order_id.currency_id
				)
		if self.order_id_stock.id:
			if not self.product_uom or not self.product_id:
				self.price_unit = 0.0
				return
			if self.order_id_stock.pricelist_id and self.order_id_stock.partner_id:
				product = self.product_id.with_context(
					lang=self.order_id_stock.partner_id.lang,
					partner=self.order_id_stock.partner_id,
					quantity=self.product_uom_qty,
					date=self.order_id_stock.date_order,
					pricelist=self.order_id_stock.pricelist_id.id,
					uom=self.product_uom.id,
					fiscal_position=self.env.context.get('fiscal_position')
				)
				self.price_unit = product._get_tax_included_unit_price(
					self.company_id or self.order_id_stock.company_id,
					self.order_id_stock.currency_id,
					self.order_id_stock.date_order,
					'sale',
					fiscal_position=self.order_id_stock.fiscal_position_id,
					product_price_unit=self._get_display_price(product),
					product_currency=self.order_id_stock.currency_id
				)
	def _get_display_price(self, product):
		if self.order_id_stock.id:
			no_variant_attributes_price_extra = [
				ptav.price_extra for ptav in self.product_no_variant_attribute_value_ids.filtered(
					lambda ptav:
						ptav.price_extra and
						ptav not in product.product_template_attribute_value_ids
				)
			]
			if no_variant_attributes_price_extra:
				product = product.with_context(
					no_variant_attributes_price_extra=tuple(no_variant_attributes_price_extra)
				)

			if self.order_id_stock.pricelist_id.discount_policy == 'with_discount':
				return product.with_context(pricelist=self.order_id_stock.pricelist_id.id, uom=self.product_uom.id).price
			product_context = dict(self.env.context, partner_id=self.order_id_stock.partner_id.id, date=self.order_id_stock.date_order, uom=self.product_uom.id)

			final_price, rule_id = self.order_id_stock.pricelist_id.with_context(product_context).get_product_price_rule(product or self.product_id, self.product_uom_qty or 1.0, self.order_id_stock.partner_id)
			base_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, self.order_id_stock.pricelist_id.id)
			if currency != self.order_id_stock.pricelist_id.currency_id:
				base_price = currency._convert(
					base_price, self.order_id_stock.pricelist_id.currency_id,
					self.order_id_stock.company_id or self.env.company, self.order_id_stock.date_order or fields.Date.today())
			# negative discounts (= surcharge) are included in the display price
			return max(base_price, final_price)
		if self.order_id.id:
			no_variant_attributes_price_extra = [
				ptav.price_extra for ptav in self.product_no_variant_attribute_value_ids.filtered(
					lambda ptav:
						ptav.price_extra and
						ptav not in product.product_template_attribute_value_ids
				)
			]
			if no_variant_attributes_price_extra:
				product = product.with_context(
					no_variant_attributes_price_extra=tuple(no_variant_attributes_price_extra)
				)

			if self.order_id.pricelist_id.discount_policy == 'with_discount':
				return product.with_context(pricelist=self.order_id.pricelist_id.id, uom=self.product_uom.id).price
			product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order, uom=self.product_uom.id)

			final_price, rule_id = self.order_id.pricelist_id.with_context(product_context).get_product_price_rule(product or self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
			base_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, self.order_id.pricelist_id.id)
			if currency != self.order_id.pricelist_id.currency_id:
				base_price = currency._convert(
					base_price, self.order_id.pricelist_id.currency_id,
					self.order_id.company_id or self.env.company, self.order_id.date_order or fields.Date.today())
			# negative discounts (= surcharge) are included in the display price
			return max(base_price, final_price)
class AccountAnalyticJournal(models.Model):
	_name = 'account.analytic.journal'

	name = fields.Char('Nombre')



class SaleReport(models.Model):
    _inherit = "sale.report"

    shop_id = fields.Many2one('account.analytic.journal', string=u'Centro')

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['shop_id'] = ", s.shop_id as shop_id"
        
        groupby += ', s.shop_id'
        
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)