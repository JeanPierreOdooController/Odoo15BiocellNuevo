# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import tools 

class stock_location(models.Model):
	_inherit  = 'stock.location'

	es_consignacion = fields.Boolean('¿Es Consignación?',default=False)

class account_analytic_journal(models.Model):
	_inherit="account.analytic.journal"

	tipo_operacion_venta = fields.Many2one('stock.picking.type','Tipo Operacion  para Cliente')
	tipo_operacion_cliente = fields.Many2one('stock.picking.type','Tipo Operacion Venta')
	

class res_partner(models.Model):
	_inherit = 'res.partner'

	es_consignacion = fields.Boolean(u'Tiene Consignación?',default=False)
	almacen_consignacion = fields.Many2one('stock.warehouse','Almacen de Consignación')
	precio_guia = fields.Boolean('Tiene Precio en Guias',default=False)

class stock_move_line(models.Model):
	_inherit = 'stock.move.line'

	qty_consumida = fields.Float('Cantidad Consumida',default=0)

	def write(self,vals):
		for i in self:
			qty_ant = i.qty_consumida
			t = super(stock_move_line,i).write(vals)
			i.refresh()
			if i.move_id.sale_id_return.user_confirmación.id and 'qty_consumida' in vals and qty_ant != i.qty_consumida:
				raise UserError('No se puede editar la cantidad de una HC aprobada.')
			

	@api.constrains('qty_consumida')
	def constraint_consumido_qty(self):
		for i in self:
			if i.state=='done' and i.qty_consumida > i.qty_done:
				raise UserError('No puede consumir mas de lo despachado')

class stock_move(models.Model):
	_inherit = 'stock.move'


	def get_packing(self):
		for i in self:
			i.paquete = i.move_line_ids[0].package_id.name if len(i.move_line_ids)!= 0 else ''
	
	sale_id_return = fields.Many2one('sale.order','Pedido de Venta',copy=False)
	consumido_qty = fields.Float('Consumido',compute="get_consumido_qty")
	paquete = fields.Char('Packing',compute="get_packing")
	price_unit_sale  = fields.Float('Price Unit Sale', compute="get_subtotal_sale")

	bio_pu = fields.Float('BIO PU', compute="get_data_bio")
	bio_cantidad = fields.Float('BIO CANTIDAD', compute="get_data_bio")
	bio_descuento = fields.Float('BIO Descuento', compute="get_data_bio")
	bio_total = fields.Float('BIO Total', compute="get_data_bio")

	def get_data_bio(self):
		for i in self:
			pedido = i.sale_line_id if i.sale_line_id.id else False
			if pedido:
				i.bio_pu = pedido.price_unit
				i.bio_cantidad = i.product_uom_qty
				i.bio_descuento = (pedido.price_reduce - pedido.price_unit)* i.product_uom_qty *-1
				i.bio_total = pedido.price_reduce * i.product_uom_qty 
			else:
				i.bio_pu = 0
				i.bio_cantidad = 0
				i.bio_descuento = 0
				i.bio_total = 0
			
	
	def get_subtotal_sale(self):
		for i in self:
			pus = 0
			sts = 0
			if i.sale_id_return.id:
				lineas = i.sale_id_return.order_line.filtered(lambda r: r.product_id.id == i.product_id.id)
				if len(lineas)>0:
					lineas = lineas[0]
					pus = lineas.price_subtotal / lineas.product_uom_qty if lineas.product_uom_qty != 0 else 0
			i.price_unit_sale = pus
			
	def write(self,vals):
		t = super(stock_move,self).write(vals)
		if 'state' in vals and vals['state']== 'done':
			for i in self:
				i.refresh()
				if i.sale_line_id.id and i.state=='done' and i.location_dest_id.id == i.sale_line_id.order_id.shop_id.tipo_operacion_venta.default_location_dest_id.id:
					i.sale_id_return =i.sale_line_id.order_id.id
		return t

	def get_consumido_qty(self):
		for i in self:
			total = 0
			for l in i.move_line_ids:
				total += l.qty_consumida
			i.consumido_qty = total

	def open_wizard_lineas(self):
		if self.sale_id_return.user_confirmación.id:
			return {
				'name': "Consumo",
				'type': 'ir.actions.act_window',			
				'view_mode': 'form',
				'view_id': self.env.ref('biocell_devoluciones_comerciales_stock.view_move_returnbio_form_onlyread').id,
				'res_model': 'stock.move',
				'res_id': self.id,
				'target': 'new',
			}
		else:
			return {
				'name': "Consumo",
				'type': 'ir.actions.act_window',			
				'view_mode': 'form',
				'view_id': self.env.ref('biocell_devoluciones_comerciales_stock.view_move_returnbio_form').id,
				'res_model': 'stock.move',
				'res_id': self.id,
				'target': 'new',
			}

class sale_order(models.Model):
	_inherit = 'sale.order'

	move_ids_return = fields.One2many('stock.move','sale_id_return','Hoja de Consumo')
	generado = fields.Boolean('Generado',default=False, tracking=True,copy=False)
	fecha_confirmación = fields.Datetime(u'Fecha Aprobación de HC', tracking=True,copy=False)
	user_confirmación = fields.Many2one('res.users',u'Usuario Aprobación de HC', tracking=True,copy=False)

	es_consignacion = fields.Boolean(related='partner_id.es_consignacion')
	almacen_consignacion = fields.Many2one(related='partner_id.almacen_consignacion')

	guia_remision_id = fields.Many2one('logistic.despatch','Guia de Remisión')
	almacen_consignacion_stock = fields.Boolean(related='warehouse_id.lot_stock_id.es_consignacion')

	def action_confirm(self):
		t = super(sale_order,self).action_confirm()
		for i in self:
			for l in i.picking_ids:
				l.do_unreserve()
				if i.shop_id.id and i.shop_id.tipo_operacion_venta.id   and i.warehouse_id.lot_stock_id.es_consignacion == False:
					self.env.cr.execute(""" update stock_picking set picking_type_id = """+str(i.shop_id.tipo_operacion_venta.id) + """ where id = """+str(l.id)+""" """)
					self.env.cr.execute(""" update stock_picking set location_id = """+str(i.shop_id.tipo_operacion_venta.default_location_src_id.id) + """ where id = """+str(l.id)+""" """)
					self.env.cr.execute(""" update stock_picking set location_dest_id = """+str(i.shop_id.tipo_operacion_venta.default_location_dest_id.id) + """ where id = """+str(l.id)+""" """)
					for m in l.move_ids_without_package:
						self.env.cr.execute(""" update stock_move set picking_type_id = """+str(i.shop_id.tipo_operacion_venta.id) + """ where id = """+str(m.id)+""" """)
						self.env.cr.execute(""" update stock_move set location_id = """+str(i.shop_id.tipo_operacion_venta.default_location_src_id.id) + """ where id = """+str(m.id)+""" """)
						self.env.cr.execute(""" update stock_move set location_dest_id = """+str(i.shop_id.tipo_operacion_venta.default_location_dest_id.id) + """ where id = """+str(m.id)+""" """)
						for xi in m.move_line_ids:								
							self.env.cr.execute(""" update stock_move_line set location_id = """+str(i.shop_id.tipo_operacion_venta.default_location_src_id.id) + """ where id = """+str(xi.id)+""" """)
							self.env.cr.execute(""" update stock_move_line set location_dest_id = """+str(i.shop_id.tipo_operacion_venta.default_location_dest_id.id) + """ where id = """+str(xi.id)+""" """)

		return t

	def crear_gr(self):
		if self.guia_remision_id.id:
			return {			
				'name': 'Guia de Remisión',
				'type': 'ir.actions.act_window',
				'res_model': 'logistic.despatch',
				'view_mode': 'form',
				'views': [(False, 'form')],
				'target': 'new',
				'res_id': self.guia_remision_id.id,
			}
		else:
			det= []
			for lin in self.order_line:
				if lin.qty_delivered >0:
					det.append(
						(0,0,{
					'product_id': lin.product_id.id,
					'name': lin.product_id.name_get()[0][1],
					'uom_id': lin.product_uom.id,
					'quantity': lin.qty_delivered,
					}) )
			nuevag = self.env['logistic.despatch'].create({
				'state':'draft',
				'l10n_pe_dte_shipment_reason':'01',
				'l10n_pe_dte_transport_mode':'02',
				'partner_id':self.partner_id.id,
				'journal_id': self.env['account.journal'].search([('l10n_pe_is_dte','=',True)]).filtered(lambda r: r.name[:2]== 'T0')[0].id if len(self.env['account.journal'].search([('l10n_pe_is_dte','=',True)]).filtered(lambda r: r.name[:2]== 'T0'))>0 else False,
				'origin_address_id': self.warehouse_id.partner_id.id,
				'delivery_address_id': self.partner_shipping_id.id,
				'line_ids':det,
				})
			self.guia_remision_id = nuevag.id
			return {			
				'name': 'Guia de Remisión',
				'type': 'ir.actions.act_window',
				'res_model': 'logistic.despatch',
				'view_mode': 'form',
				'views': [(False, 'form')],
				'target': 'new',
				'res_id': nuevag.id,
			}

	"""
	@api.onchange('partner_id')
	def onchange_partner_id_consignacion(self):
		for i in self:
			if i.partner_id.es_consignacion:
				i.warehouse_id = i.partner_id.almacen_consignacion.id
	"""

	def aprobarhc(self):
		import datetime
		if self.env.user.has_group('biocell_devoluciones_comerciales_stock.group_aprobadores_hc'):				
			if self.user_confirmación.id:
				raise UserError('Ya esta aprobado')
			self.fecha_confirmación = datetime.datetime.now()
			self.user_confirmación = self.env.user.id
		else:
			raise UserError('No es un usuario con los privilegios para Aprobar HC')


	def desaprobarhc(self):
		import datetime
		if self.env.user.has_group('biocell_devoluciones_comerciales_stock.group_aprobadores_hc'):				
			if not self.user_confirmación.id:
				raise UserError('No esta aprobado')
			if self.generado:
				raise UserError('Ya se encuentra generado el retorno')
			self.fecha_confirmación = False
			self.user_confirmación = False
		else:
			raise UserError('No es un usuario con los privilegios para Desaprobar HC')


	def generate_dev(self):
		if self.generado:
			raise UserError('Ya se genero el retorno')
		if not self.user_confirmación.id:
			raise UserError('No se encuentra aprobado la HC')

		self.generado = True
		pickings = self.move_ids_return.mapped('picking_id')
		picking_dev = {}
		line_dev = {}
		for i in pickings:
			dev_w = self.env['stock.return.picking'].with_context({'active_id':i.id,'active_model':'stock.picking'}).create({'picking_id':i.id})
			dev_w._onchange_picking_id()
			for elem in dev_w.product_return_moves:
				elem.quantity= 0
			for gg in self.move_ids_return.filtered(lambda pp: pp.picking_id.id == i.id):
				linea_dev = dev_w.product_return_moves.filtered(lambda mm : mm.move_id.id == gg.id)
				pickings_total = self.picking_ids.mapped('move_ids_without_package').filtered(lambda r: r.product_id.id == gg.product_id.id and r.state == 'done' and r.location_id.id == gg.location_dest_id.id and r.location_dest_id.id == gg.location_id.id and r.origin_returned_move_id.id ==gg.id)
				retornados = 0
				for elemxy in pickings_total:
					retornados += elemxy.quantity_done
				linea_dev.quantity = gg.quantity_done - retornados
			flagxyz = False
			for xyz in dev_w.product_return_moves:
				if xyz.quantity >0:
					flagxyz = True
			if flagxyz:
				devolucion = dev_w.create_returns()
				picking_deb = self.env['stock.picking'].browse(devolucion['res_id'])
				picking_deb.move_line_ids_without_package.unlink()
				for elemx in self.move_ids_return.filtered(lambda pp: pp.picking_id.id == i.id):
					nuevaline =  picking_deb.move_ids_without_package.filtered(lambda xx: xx.origin_returned_move_id.id == elemx.id )
					line_dev[elemx.id] = nuevaline.id
					
	
				for gg in self.move_ids_return.filtered(lambda pp: pp.picking_id.id == i.id):
					for lotes in gg.move_line_ids:
						move_id_llenar = picking_deb.move_ids_without_package.filtered(lambda xx : xx.origin_returned_move_id.id == gg.id)						
						if len(move_id_llenar)>0:
							move_id_llenar =move_id_llenar[0]
							data = {
								'move_id':move_id_llenar.id,
								'picking_id':move_id_llenar.picking_id.id,
								'product_id':move_id_llenar.product_id.id,
								'location_id':move_id_llenar.location_id.id,
								'location_dest_id':move_id_llenar.location_dest_id.id,
								'product_uom_id':move_id_llenar.product_uom.id,
								'qty_done':lotes.qty_done,
								'state':'assigned',
								'lot_id':lotes.lot_id.id,
								'package_id':lotes.result_package_id.id,
								'result_package_id':lotes.package_id.id,
								'company_id':move_id_llenar.company_id.id,
							}
							self.env['stock.move.line'].create(data)
							
				respuesta =picking_deb.button_validate()
	
				if  respuesta and str(type(respuesta)) == "<class 'dict'>" and  'res_model' in respuesta and respuesta['res_model'] == 'expiry.picking.confirmation' :
					nuevo = self.env['expiry.picking.confirmation'].with_context(respuesta['context']).create({})
					nuevo.process()
				picking_dev[i.id] = picking_deb.id
			
		nuevoalb = False
		for i in pickings:
			if i.id in picking_dev:
				dev_w = self.env['stock.return.picking'].with_context({'active_id':picking_dev[i.id],'active_model':'stock.picking'}).create({'picking_id':picking_dev[i.id]})
				dev_w._onchange_picking_id()
				for elem in dev_w.product_return_moves:
					elem.quantity= 0
				algo = False
				for gg in self.move_ids_return.filtered(lambda pp: pp.picking_id.id == i.id and pp.consumido_qty > 0):
					linea_dev = dev_w.product_return_moves.filtered(lambda mm : mm.move_id.id == line_dev[gg.id])
					if len(linea_dev)>0:
						linea_dev.quantity = gg.consumido_qty
						algo = True
				if algo:
					devolucion = dev_w.create_returns()
					picking_deb = self.env['stock.picking'].browse(devolucion['res_id'])
					
					if self.shop_id.id and self.shop_id.tipo_operacion_cliente.id:
						self.env.cr.execute(""" update stock_picking set picking_type_id = """+str(self.shop_id.tipo_operacion_cliente.id) + """ where id = """+str(picking_deb.id)+""" """)
						self.env.cr.execute(""" update stock_picking set location_dest_id = """+str(self.shop_id.tipo_operacion_cliente.default_location_dest_id.id) + """ where id = """+str(picking_deb.id)+""" """)
						for m in picking_deb.move_ids_without_package:
							self.env.cr.execute(""" update stock_move set picking_type_id = """+str(self.shop_id.tipo_operacion_cliente.id) + """ where id = """+str(m.id)+""" """)
							self.env.cr.execute(""" update stock_move set location_dest_id = """+str(self.shop_id.tipo_operacion_cliente.default_location_dest_id.id) + """ where id = """+str(m.id)+""" """)
		
					picking_deb.move_line_ids_without_package.unlink()
		
					for gg in self.move_ids_return.filtered(lambda pp: pp.picking_id.id == i.id and pp.consumido_qty >0):
						for lotes in gg.move_line_ids:
							
							move_id_llenar = picking_deb.move_ids_without_package.filtered(lambda xx : xx.origin_returned_move_id.id == line_dev[gg.id] )
							if len(move_id_llenar)>0:
								move_id_llenar =move_id_llenar[0]
								move_id_llenar.refresh()
								data = {
									'move_id':move_id_llenar.id,
									'picking_id':move_id_llenar.picking_id.id,
									'product_id':move_id_llenar.product_id.id,
									'location_id':move_id_llenar.location_id.id,
									'location_dest_id':move_id_llenar.location_dest_id.id,
									'product_uom_id':move_id_llenar.product_uom.id,
									'qty_done':lotes.qty_consumida,
									'state':'assigned',
									'lot_id':lotes.lot_id.id,
									'package_id':lotes.package_id.id,
									'company_id':move_id_llenar.company_id.id,
								}
								self.env['stock.move.line'].create(data)
					respuesta =picking_deb.button_validate()
	
					if respuesta and str(type(respuesta)) == "<class 'dict'>" and 'res_model' in respuesta and respuesta['res_model'] == 'expiry.picking.confirmation' :
						nuevo = self.env['expiry.picking.confirmation'].with_context(respuesta['context']).create({})
						nuevo.process()
	
					if nuevoalb == False:
						nuevoalb = picking_deb
						nuevoalb.origin = ''
						self.env.cr.execute(""" update stock_move set kardex_date = kardex_date + interval '1 second' where picking_id = """+str(picking_deb.id) + """ ;""")
						self.env.cr.execute(""" update stock_picking set kardex_date = kardex_date + interval '1 second' where id = """+str(picking_deb.id) + """ ;""")
		
					if nuevoalb.id != picking_deb.id:
						self.env.cr.execute(""" update stock_move_line set picking_id = """ +str(nuevoalb.id)+ """ where picking_id = """+str(picking_deb.id) + """ ;""")
						self.env.cr.execute(""" update stock_move set picking_id = """ +str(nuevoalb.id)+ """ where picking_id = """+str(picking_deb.id) + """ ;""")
						self.env.cr.execute(""" delete from stock_picking where id = """ +str(picking_deb.id) + """ ;""")
		
class sale_order_line(models.Model):
	_inherit = 'sale.order.line'

	@api.model
	def create(self,vals):
		t=super(sale_order_line,self).create(vals)
		if t.order_id.state in ('done','sale')  and t.order_id.generado==False:
			for picking in t.order_id.picking_ids:
				i = t.order_id
				l = picking
				if i.shop_id.id and i.shop_id.tipo_operacion_venta.id and l.state not in ('done','cancel')  and i.warehouse_id.lot_stock_id.es_consignacion == False:
					self.env.cr.execute(""" update stock_picking set picking_type_id = """+str(i.shop_id.tipo_operacion_venta.id) + """ where id = """+str(l.id)+""" """)
					self.env.cr.execute(""" update stock_picking set location_dest_id = """+str(i.shop_id.tipo_operacion_venta.default_location_dest_id.id) + """ where id = """+str(l.id)+""" """)
					for m in l.move_ids_without_package:
						self.env.cr.execute(""" update stock_move set picking_type_id = """+str(i.shop_id.tipo_operacion_venta.id) + """ where id = """+str(m.id)+""" """)
						self.env.cr.execute(""" update stock_move set location_dest_id = """+str(i.shop_id.tipo_operacion_venta.default_location_dest_id.id) + """ where id = """+str(m.id)+""" """)
						for xi in m.move_line_ids:								
							self.env.cr.execute(""" update stock_move_line set location_dest_id = """+str(i.shop_id.tipo_operacion_venta.default_location_dest_id.id) + """ where id = """+str(xi.id)+""" """)
			listos = None
			for picking in t.order_id.picking_ids:
				if picking.state in ('confirmed','assigned'):
					if listos == None:
						listos = picking.id
					if listos > picking.id:
						listos = picking.id
			if listos != None:
				for picking in t.order_id.picking_ids:
					if picking.state in ('confirmed','assigned') and picking.id != listos:
						self.env.cr.execute(""" update stock_move set picking_id = """+str(listos)+""" where picking_id = """+str(picking.id)+""" """)
						self.env.cr.execute(""" update stock_move_line set picking_id = """+str(listos)+""" where picking_id = """+str(picking.id)+""" """)						
						self.env.cr.execute(""" delete from stock_picking where id = """+str(picking.id)+""" """)						
				
		return t

	def write(self,vals):
		t=super(sale_order_line,self).write(vals)
		if self.order_id.state in ('done','sale') and self.order_id.generado==False:
			for picking in self.order_id.picking_ids:
				i = self.order_id
				l = picking
				if i.shop_id.id and i.shop_id.tipo_operacion_venta.id and l.state not in ('done','cancel')  and i.warehouse_id.lot_stock_id.es_consignacion == False:
					self.env.cr.execute(""" update stock_picking set picking_type_id = """+str(i.shop_id.tipo_operacion_venta.id) + """ where id = """+str(l.id)+""" """)
					self.env.cr.execute(""" update stock_picking set location_dest_id = """+str(i.shop_id.tipo_operacion_venta.default_location_dest_id.id) + """ where id = """+str(l.id)+""" """)
					for m in l.move_ids_without_package:
						self.env.cr.execute(""" update stock_move set picking_type_id = """+str(i.shop_id.tipo_operacion_venta.id) + """ where id = """+str(m.id)+""" """)
						self.env.cr.execute(""" update stock_move set location_dest_id = """+str(i.shop_id.tipo_operacion_venta.default_location_dest_id.id) + """ where id = """+str(m.id)+""" """)
						for xi in m.move_line_ids:								
							self.env.cr.execute(""" update stock_move_line set location_dest_id = """+str(i.shop_id.tipo_operacion_venta.default_location_dest_id.id) + """ where id = """+str(xi.id)+""" """)
				
		return t


class facturacion_venta_pendiente(models.Model):
	_name = 'facturacion.venta.pendiente'

	pedido = fields.Many2one('sale.order','Pedido')
	partner = fields.Many2one('res.partner','Cliente')
	date_order = fields.Datetime('Fecha Pedido')
	currency_id = fields.Many2one('res.currency','Moneda')
	producto = fields.Many2one('product.product','Producto')
	entregado = fields.Float('Entregado')
	pu = fields.Float('Precio Unitario')
	subtotal = fields.Float('Subtotal')

	_auto = False


	def init(self):
		tools.drop_view_if_exists(self.env.cr, self._table)
		self.env.cr.execute('''
			CREATE OR REPLACE VIEW %s AS (
				SELECT 
					sol.id,
					so.id as pedido,
     					so.partner_id as partner,
					so.date_order,
					ppl.currency_id,
					sol.product_id as producto,
					(coalesce(sol.qty_delivered,0) - coalesce(sol.qty_invoiced,0)) as entregado,
					sol.price_unit as pu,
					(coalesce(sol.qty_delivered,0) - coalesce(sol.qty_invoiced,0)) * sol.price_unit as subtotal
				from sale_order so
				inner join sale_order_line sol on sol.order_id = so.id
				inner join product_pricelist ppl on ppl.id = so.pricelist_id
				where so.state in ('sale','done')
				and (coalesce(sol.qty_delivered,0) - coalesce(sol.qty_invoiced,0)) > 0
				and coalesce(so.generado,false) = true			
			)''' % (self._table,)
		)

class account_move(models.Model):
	_inherit = 'account.move'

	paciente_rel = fields.Char('Paciente',compute="get_saleinfo")
	doctor_rel =  fields.Char('Doctor',compute="get_saleinfo")

	paciente_personalizado = fields.Char('Paciente Personalizado')
	doctor_personalizado = fields.Many2one('res.partner','Doctor Personalizado')

	def get_saleinfo(self):
		for i in self:
			pa = False
			do = False
			pedido = False
			for l in i.invoice_line_ids:
				for k in l.sale_line_ids:
					pedido = k.order_id
			if pedido:
				pa = pedido.name_patient
				do = pedido.name_doctor.name_get()[0][1] if pedido.name_doctor.id else False
			else:
				pa = i.paciente_personalizado
				do = i.doctor_personalizado.name_get()[0][1] if i.doctor_personalizado.id else False
			i.paciente_rel = pa
			i.doctor_rel = do




class account_move_line(models.Model):
	_inherit = 'account.move.line'

	categoria = fields.Many2one('product.category',related='product_id.categ_id',string="Categoria")



