# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CostsSalesAnalysisBookAdjustmBiocell(models.Model):
	_name = 'costs.sales.analysis.book.adjustm.biocell'
	_auto = False
	
	fecha = fields.Date(string=u'Fecha')
	almacen = fields.Char(string=u'Almacén')
	origen = fields.Char(string=u'Origen')
	destino = fields.Char(string=u'Destino')
	doc = fields.Char(string=u'Documento')
	operation_type = fields.Char(string=u'TD')
	serial = fields.Char(string=u'Serie')
	nro = fields.Char(string=u'Número')
	product_id = fields.Many2one('product.product')
	default_code = fields.Char(string="Código de Producto")
	producto = fields.Char(string=u'Producto')
	lote = fields.Char(string=u'Lote')
	cantidad = fields.Float(string='Cantidad', digits=(64,2))
	valor = fields.Float(string='Valor', digits=(64,2))
	valuation_account_id = fields.Many2one('account.account',string=u'Cuenta Producto')
	input_account_id = fields.Many2one('account.account',string=u'Cuenta Variación')
	output_account_id = fields.Many2one('account.account',string=u'Cuenta Costo de Venta')