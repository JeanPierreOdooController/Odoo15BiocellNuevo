# -- coding: utf-8 --

from odoo import models, fields, api
from odoo.exceptions import UserError

class stock_move(models.Model):
	_inherit = "stock.move"

	lot_id = fields.Char('Lotes',compute="get_lot_id_rel")
	
	fecha_vencimiento = fields.Char('Expiración',compute="get_lot_id_rel")

	def get_lot_id_rel(self):
		for i in self:
			data = ""
			fecha = ""
			for l in i.move_line_ids:
				if l.lot_id.id:
					data+=  l.lot_id.name if data == "" else (', '+ l.lot_id.name)
					fecha+=  str(l.lot_id.expiration_date or "")[:10] if fecha == "" else (', '+ str(l.lot_id.expiration_date or "")[:10] )
			i.lot_id = data
			i.fecha_vencimiento = fecha


	tipo_product = fields.Selection (related="product_id.detailed_type", string="Tipo")


	


class stock_picking(models.Model):
	_inherit = "stock.picking"

	name_patient = fields.Char(compute="get_data_venta", string="Nombre paciente")
	patient_vat = fields.Char(compute="get_data_venta", string="Paciente DNI/RUC")
	clinic_history = fields.Char(compute="get_data_venta", string="Historial Clinico")
	medic_center = fields.Char(compute="get_data_venta", string="Centro medico")
	name_doctor = fields.Char(compute="get_data_venta", string="Nombre doctor")
	sugery_date = fields.Datetime(compute="get_data_venta", string="Fecha/hora cirugia")
	sugery_order = fields.Char(compute="get_data_venta", string="Orden cirugia")
	procedure_clinic = fields.Char(compute="get_data_venta", string="Procedimiento clinico")
	procedure_clinic_id = fields.Many2one('procedure.clinic', compute="get_data_venta", string="Procedimiento clinico")
	instrumentalist = fields.Char(compute="get_data_venta", string="Instrumentista")
	request_date = fields.Datetime(compute="get_data_venta", string="fecha solicitud de cotizacion")
	schedulling_request_date = fields.Datetime(compute="get_data_venta", string="fecha solicitud de agendamiento")
	user_id_sale = fields.Many2one('res.users',compute="get_data_venta", string="Vendedor")
	shop_id = fields.Char(compute="get_data_venta", string="Centro")
	categoria_rel = fields.Char('Categoria',compute="get_categoria_rel")
	name_sale = fields.Char(compute="get_data_venta", string='Orden de Venta')
	payment_term_id = fields.Char(compute="get_data_venta", string="Forma de Pago")
	cod_cirugia = fields.Char(string="Código de Cirugia")
	nro_gaveta = fields.Char(string="Nro. de Gaveta")

	def get_data_venta(self):
		for i in self:
			pedido = False
			for l in i.move_ids_without_package:
				if l.sale_line_id.id:
					pedido = l.sale_line_id.order_id
			if pedido:

				i.name_patient = pedido.name_patient
				i.patient_vat = pedido.patient_vat
				i.clinic_history = pedido.clinic_history
				i.medic_center = pedido.medic_center.name_get()[0][1] if pedido.medic_center.id else False
				i.name_doctor = pedido.name_doctor.name
				i.sugery_date = pedido.sugery_date
				i.sugery_order = pedido.sugery_order
				i.procedure_clinic = pedido.procedure_clinic_id.name
				i.procedure_clinic_id = pedido.procedure_clinic_id.id
				i.instrumentalist = pedido.instrumentalist.name
				i.request_date = pedido.request_date
				i.schedulling_request_date = pedido.schedulling_request_date
				i.user_id_sale = pedido.user_id.id
				i.shop_id = pedido.shop_id.name
				i.name_sale = pedido.name
				i.payment_term_id = pedido.payment_term_id.name

			else:
				
				i.name_patient = False
				i.patient_vat = False
				i.clinic_history = False
				i.medic_center = False
				i.name_doctor = False
				i.sugery_date = False
				i.sugery_order = False
				i.procedure_clinic = False
				i.procedure_clinic_id = False
				i.instrumentalist = False
				i.request_date = False
				i.schedulling_request_date = False
				i.user_id_sale = False
				i.shop_id = False
				i.name_sale = False
				i.payment_term_id = False

	def get_categoria_rel(self):
		for i in self:
			data = ""
			categorias = []
			for l in i.move_ids_without_package:
				if l.product_id.categ_id.id in categorias:
					pass
				else:
					categorias.append(l.product_id.categ_id.id)
					data += l.product_id.categ_id.name if data == "" else (', '+ l.product_id.categ_id.name)
			i.categoria_rel=data
