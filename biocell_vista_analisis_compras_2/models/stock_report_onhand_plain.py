# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools

class stock_report_onhand_purchase_plain(models.Model):
	_name = 'stock.report.onhand.purchase.plain'
	_description = 'BackOrder Compras - Reporte plano'
	_auto = False

	purchase_name=fields.Char('Nro. de Pedido de Compra')
	partner_id=fields.Many2one('res.partner','Proveedor') 
	partner_ref=fields.Char('Nro. Orden de Cotización proveedor')
	invoice_number=fields.Char('Nro. de Factura')
	nro_guia_compra=fields.Char(u'Nro. Guía de Remisión')
	date_order=fields.Datetime('Fecha de pedido')
	date_invoice=fields.Date('Fecha de factura')
	date_picking=fields.Datetime(u'Fecha de Albarán de ingreso')
	product_id = fields.Many2one('product.product','Producto')
	qty_req=fields.Float('Cantidad solicitada',related='purchase_line_id.product_qty')
	qty_received=fields.Float('Cantidad Entregada',related='purchase_line_id.qty_received')
	qty_waiting=fields.Float('Cantidad pendiente',compute='get_qtywaitng')
	purchase_id=fields.Many2one('purchase.order','Compra')
	purchase_line_id=fields.Many2one('purchase.order.line','Linea de Compra')
	picking_id=fields.Many2one('stock.picking','Albaran')
	stock_move_id=fields.Many2one('stock.move','moviento de almacen')
	invoice_id=fields.Many2one('account.move','Factura')
	account_move_line_id=fields.Many2one('account.move.line','Linea de factura')
	company_id=fields.Many2one('res.company',u'Compañía')

	def get_qtywaitng(self):
		for l in self:
			l.qty_waiting=l.qty_req-l.qty_received


	def init(self):
		tools.drop_view_if_exists(self._cr, 'stock_report_onhand_purchase_plain')
		cadsql="""
			CREATE or REPLACE VIEW stock_report_onhand_purchase_plain AS (
			select 
			row_number() OVER () AS id,
			purchase_order.name as purchase_name,
			purchase_order.partner_id, 
			purchase_order.partner_ref, 
			account_move.ref as invoice_number,
			stock_picking.nro_guia_compra,
			purchase_order.date_approve as date_order,
			account_move.invoice_date as date_invoice,			
			stock_picking.date_done as date_picking,
			purchase_order_line.product_id as product_id,
			purchase_order.id as purchase_id,
			purchase_order_line.id as purchase_line_id,
			stock_picking.id as picking_id,
			stock_move.id as stock_move_id,
			account_move.id as invoice_id,			
			account_move_line.id as account_move_line_id,
			purchase_order.company_id as company_id
			from purchase_order
			inner join purchase_order_line on purchase_order.id = purchase_order_line.order_id
			left join account_move_line on purchase_order_line.id = account_move_line.purchase_line_id
			left join account_move on account_move_line.move_id = account_move.id
			left join stock_move on purchase_order_line.id=stock_move.purchase_line_id
			left join stock_picking on stock_move.picking_id=stock_picking.id
			where purchase_order.state in ('purchase','done'));
		"""
		self.env.cr.execute(cadsql)