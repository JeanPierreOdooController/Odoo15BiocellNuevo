# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMainParameter(models.Model):
	_inherit = 'account.main.parameter'
	
	account_cost_sale_id = fields.Many2one('account.account', string='Cuenta de Costo de Ventas')
	location_ids_csa_adjustm = fields.Many2many('stock.location', 'stock_location_warehouse_adjustm_parameter_rel', string=u'Ubicación Origen Ajuste')
	location_dest_ids_csa_adjustm = fields.Many2many('stock.location', 'stock_location_dest_warehouse_adjustm_parameter_rel', string=u'Ubicación Destino Ajuste')
	operation_type_ids_csa_adjustm = fields.Many2many('type.operation.kardex', 'type_operation_kardex_csa_adjustm_warehouse_parameter_rel', string=u'Tipo de Operación Ajuste')
	cs_date_by_invoice_date = fields.Boolean(string='Mostrar Costo de Venta en base a Fecha Factura',default=False)