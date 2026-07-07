# -*- coding:utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class account_move(models.Model):
	_inherit = 'account.move'

	picking_ids = fields.One2many('stock.picking','invoice_id','Albaranes')

class biocell_panel_saldos_financieros_4_lote_wizard_clinica(models.TransientModel):
	_name = 'stock.balance.report.lote.wizard.clinica'
	_description = "stock balance report lote wizard clinica"

	def get_stock_lote(self):
		return self.env['stock.balance.report.lote.clinica'].with_context({'res_model_it':'stock.balance.report.lote.wizard.clinica','id_it':self.id}).get_balance_view()


class StockBalanceReportLoteclinica(models.Model):
	_name = 'stock.balance.report.lote.clinica'
	_description = 'Balance Report Lote clinica'

	producto = fields.Many2one('product.product',string='N.Producto',store=True)
	codigo = fields.Char(related='producto.default_code',string='Cod. Producto',store=True)
	almacen = fields.Many2one('res.partner',string=u'N.Almacén',store=True)
	entrada = fields.Float(string='Stock', digits=(12,2),store=True)
	salida = fields.Float(string='Salida', digits=(12,2),store=True)
	saldo = fields.Float(string='Disponible', digits=(12,2),store=True)
	unidad = fields.Many2one(related='producto.uom_id',string='Unidad',store=True)
	categoria_1 = fields.Char(related='producto.categ_id.name',string='Categoria 1',store=True)
	categoria_2 = fields.Char(related='producto.categ_id.parent_id.name',string='Categoria 2',store=True)
	categoria_3 = fields.Char(related='producto.categ_id.parent_id.parent_id.name',string='Categoria 3',store=True)
	lote = fields.Many2one('stock.production.lot',string='Lote',store=True)
	order_id = fields.Many2one('sale.order',string='Pedido Venta',store=True)
	fecha_venc = fields.Datetime(related='lote.expiration_date',string='Fecha Vencimiento',store=True)
	invoice_ids = fields.Many2many(related='order_id.invoice_ids',string="Facturas")
	reservado = fields.Float(string='Reservado', digits=(12,2),store=True)
	product_id = fields.Many2one('product.product','Producto',store=True)
	almacen_id = fields.Many2one('res.partner','Almacen',store=True)

	def get_balance_view(self):

		tiempo_inicial = datetime.now()
		self.search([]).unlink()
		s_prod = [-1,-1,-1]
		s_loca = [-1,-1,-1]
		locat_ids = self.env['stock.location'].search( [('usage','in',('internal','internal'))] )
		lst_locations = locat_ids.ids
		productos='{'
		almacenes='{'
		lst_products = self.env['product.product'].with_context(active_test=False).search([]).ids
		if len(lst_products) == 0:
			raise UserError('Alerta','No existen productos seleccionados')

		for producto in lst_products:
			productos=productos+str(producto)+','
			s_prod.append(producto)
		productos=productos[:-1]+'}'
		for location in lst_locations:
			almacenes=almacenes+str(location)+','
			s_loca.append(location)
		almacenes=almacenes[:-1]+'}'

		config = self.env['kardex.parameter'].search([('company_id','=',self.env.company.id)])

		date_fin = self.env.context['date_final'] if 'date_final' in self.env.context else fields.Date.context_today(self)
		date_ini = '%d-01-01' % ( config._get_anio_start(date_fin.year) )

		
		#data={}
		
		#tiempo_pasado = divmod((datetime.now()-tiempo_inicial).seconds,60)
		text_report = "<b>Generando Reporte de Saldos por Lote</b><br/>"
		text_report_line = text_report + u"---Extrayendo información de la Base de Datos---"

		self.send_message(text_report_line)



		self.env.cr.execute("""
			select 
			vstf.p_id,
			vstf.alm_id,
			coalesce(sum(coalesce(vstf.entrada,0)),0) -  coalesce(sum(coalesce(vstf.salida,0)),0),
			0 as salida,
			coalesce(sum(coalesce(vstf.entrada,0)),0) -  coalesce(sum(coalesce(vstf.salida,0)),0),
			vstf.lote_id,
			0,
			vstf.p_id,
			vstf.alm_id,
			vstf.order_id
			from
			( 
			select rp.id as alm_id, vst_kardex_fisico.product_id as p_id, vst_kardex_fisico.categoria_id, vst_kardex_fisico.date as fecha,vst_kardex_fisico.u_origen as origen, vst_kardex_fisico.u_destino as destino, vst_kardex_fisico.u_destino as almacen, vst_kardex_fisico.product_qty as entrada, 0 as salida,vst_kardex_fisico.id  as stock_move,vst_kardex_fisico.guia as motivo_guia, vst_kardex_fisico.producto,vst_kardex_fisico.estado,vst_kardex_fisico.name, vst_kardex_fisico.cod_pro, vst_kardex_fisico.categoria, vst_kardex_fisico.unidad,vst_kardex_fisico.product_id,rp.id as almacen_id, vst_kardex_fisico.lote,vst_kardex_fisico.lote_id, sol.order_id from vst_kardex_fisico_lote() as vst_kardex_fisico
			left join stock_move sm on sm.id = vst_kardex_fisico.id
			left join stock_picking sp on sp.id = sm.picking_id
			left join sale_order_line sol on sol.id = sm.sale_line_id
			left join res_partner rp on rp.id = sp.partner_id
			 where vst_kardex_fisico.company_id = """+str(self.env.company.id)+"""
			and vst_kardex_fisico.location_dest_id = 39
			and (vst_kardex_fisico.date - interval '5' hour)::date >='""" +str(date_ini)+ """' and (vst_kardex_fisico.date - interval '5' hour)::date <='""" +str(date_fin)+ """'
			
			union all


			select rp.id as alm_id, vst_kardex_fisico.product_id as p_id, vst_kardex_fisico.categoria_id, vst_kardex_fisico.date as fecha,vst_kardex_fisico.u_origen as origen, vst_kardex_fisico.u_destino as destino, vst_kardex_fisico.u_origen as almacen, 0 as entrada, vst_kardex_fisico.product_qty as salida,vst_kardex_fisico.id  as stock_move ,vst_kardex_fisico.guia as motivo_guia ,vst_kardex_fisico.producto ,vst_kardex_fisico.estado,vst_kardex_fisico.name, vst_kardex_fisico.cod_pro, vst_kardex_fisico.categoria, vst_kardex_fisico.unidad,vst_kardex_fisico.product_id, rp.id as almacen_id, vst_kardex_fisico.lote, vst_kardex_fisico.lote_id,sol.order_id from vst_kardex_fisico_lote() as vst_kardex_fisico 
			left join stock_move sm on sm.id = vst_kardex_fisico.id
			left join stock_picking sp on sp.id = sm.picking_id
			left join sale_order_line sol on sol.id = sm.sale_line_id
			left join res_partner rp on rp.id = sp.partner_id			
			where vst_kardex_fisico.company_id = """+str(self.env.company.id)+"""
			and vst_kardex_fisico.location_id = 39
			and (vst_kardex_fisico.date - interval '5' hour)::date >='""" +str(date_ini)+ """' and (vst_kardex_fisico.date - interval '5' hour)::date <='""" +str(date_fin)+ """'
			
			) as vstf
			left join stock_production_lot spl on spl.id = vstf.lote_id			
			where 
			vstf.product_id in """ +str(tuple(s_prod))+ """
			and vstf.estado = 'done'
			group by
			producto,cod_pro,categoria_id, p_id, alm_id,lote,lote_id, order_id
			having coalesce(sum(coalesce(vstf.entrada,0)),0) -  coalesce(sum(coalesce(vstf.salida,0)),0) != 0
			;
		""")

		todos = self.env.cr.fetchall()

		text_report_line = text_report + u"---Se procesaran: "+ str(len(todos)) + " lineas---"
		self.send_message(text_report_line)
		cont_report = 0

		for item in todos:
			data = {
				'producto':item[0],
				'almacen':item[1],
				'entrada':item[2],
				'salida':item[3],
				'saldo':item[4],
				'lote':item[5],
				'reservado':item[6],
				'product_id':item[7],
				'almacen_id':item[8],
				'order_id':item[9],
			}
			self.env['stock.balance.report.lote.clinica'].create(data)

			if cont_report%300 == 0:
				tiempo_pasado = divmod((datetime.now()-tiempo_inicial).seconds,60)
				
				text_report_line = "<b>Generando Saldos por Lotes.</b><br/><center>Total lineas a procesar: "+str(len(todos)) + "</center><br/><center>Procesado:"+str(cont_report)+"/"+str(len(todos))+"</center><br/> Tiempo Procesado: "+ str(tiempo_pasado[0])+" minutos " +str(tiempo_pasado[1]) + " segundos" 
				text_report_line += """<div id="myProgress" style="position: relative; width: 100%;  height: 30px;   background-color: white;">
				  <div id="myBar" style="position: absolute;  width: """+"%.2f"%(cont_report*100/len(todos))+"""%;  height: 100%; background-color: #875A7B;">
				    <div id="label" style="text-align: center; line-height: 30px; color: white;">""" +"%.2f"%(cont_report*100/len(todos))+ """%</div>
				  </div>
				</div>"""
				self.send_message(text_report)

			cont_report += 1
		
		#for line in self.env.cr.fetchall():
		#	if (line[14],line[13],line[16]) in data:
		#		data[(line[14],line[13],line[16])][2] += (line[10] or 0) - (line[11] or 0)
		#	else:
		#		data[(line[14],line[13],line[16])] = [line[14],line[13], (line[10] or 0) - (line[11] or 0) , line[16], line[17],line[18] ]


		#for final in data:
		#	self.create({
		#				'producto': data[final][1],
		#				'almacen': data[final][0],
		#				'entrada': data[final][2],
		#				'salida': 0,
		#				'saldo': data[final][2]- (data[final][4] or 0),
		#				'lote': data[final][3],
		#				'reservado': data[final][4],
		#				'product_id': data[final][1],
		#				'almacen_id': data[final][0],
		#			})

		return {
			'name': 'Reporte de Saldos x Lote',
			'type': 'ir.actions.act_window',
			'res_model': 'stock.balance.report.lote.clinica',
			'view_mode': 'tree,pivot,graph',
			'views': [(False, 'tree'), (False, 'pivot'), (False, 'graph')]
		}
