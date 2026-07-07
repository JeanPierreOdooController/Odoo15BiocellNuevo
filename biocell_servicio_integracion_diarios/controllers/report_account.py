from odoo import http

from odoo import http
from odoo.http import request,Response
import json
from datetime import datetime



class Report_account(http.Controller):
	@http.route('/api/webservice/report_diary', auth="none", type='json', methods=['POST'], csrf=False)
	def get_repot_diary(self, **kw):
		if kw.get('company'):
			company = request.env['res.company'].sudo().search([('vat', '=', str(kw.get('company')))], limit=1)
			if not company:
				return {
					'status': 'error',
					'message': 'Falta la empresa.',      
				}
			if not kw.get('date_start') or not kw.get('date_end'):
				return {
				'status': 'error',
				'message': 'Faltan las fechas de inicio y fin.',        
			}

			date_start = kw.get('date_start')
			date_end = kw.get('date_end')
			date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
			date_end = datetime.strptime(date_end, '%Y-%m-%d').date()
			query = """
					SELECT
						vst1.periodo::character varying,vst1.fecha,vst1.libro,vst1.voucher,
						vst1.cuenta,vst1.debe,vst1.haber,vst1.balance,
						vst1.moneda,vst1.tc,vst1.importe_me,vst1.cta_analitica,
						regexp_replace(vst1.glosa, '[^a-zA-Z0-9-]', '', 'g') as glosa,
						vst1.td_partner,vst1.doc_partner,vst1.partner,
						vst1.td_sunat,vst1.nro_comprobante,vst1.fecha_doc,vst1.fecha_ven,
						vst1.col_reg,vst1.monto_reg,vst1.medio_pago,vst1.ple_diario,
						vst1.ple_compras,vst1.ple_ventas
						FROM get_diariog('%s','%s',%d) vst1
			"""% (date_start, date_end,company.id)
			request.env.cr.execute(query)
			columns = [desc[0] for desc in request.env.cr.description]
			rows = request.env.cr.fetchall()
			result = [dict(zip(columns, row)) for row in rows]

			return {
                'status': 'success',
                'message': 'Datos enviados correctamente.',
                'columns': columns,
                'result': result,
            }


	@http.route('/api/webservice/report_maturity_payable', auth="none", type='json', methods=['POST'], csrf=False)
	def get_report_maturity_payable(self, **kw):
		if kw.get('company'):
			company = request.env['res.company'].sudo().search([('vat', '=', str(kw.get('company')))], limit=1)
			if not company:
				return {
					'status': 'error',
					'message': 'Falta la empresa.',      
				}
			if not kw.get('date_start') or not kw.get('date_end'):
				return {
				'status': 'error',
				'message': 'Faltan las fechas de inicio y fin.',        
			}

			date_start = kw.get('date_start')
			date_end = kw.get('date_end')
			date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
			date_end = datetime.strptime(date_end, '%Y-%m-%d').date()
			query = """
					SELECT row_number() OVER () AS id,
						fecha_emi, fecha_ven, cuenta, divisa, tdp, 
						doc_partner, partner, td_sunat, nro_comprobante, 
						saldo_mn, saldo_me, cero_treinta, treinta1_sesenta, 
						sesenta1_noventa, noventa1_ciento20, ciento21_ciento50, 
						ciento51_ciento80, ciento81_mas
						FROM get_maturity_analysis('%s','%s',%s,'%s')
				"""% (date_start, date_end,company.id, 'payable')
			request.env.cr.execute(query)
			columns = [desc[0] for desc in request.env.cr.description]
			rows = request.env.cr.fetchall()
			result = [dict(zip(columns, row)) for row in rows]

			return {
                'status': 'success',
                'message': 'Datos enviados correctamente.',
                'columns': columns,
                'result': result,
            }
	@http.route('/api/webservice/report_maturity_receivable', auth="none", type='json', methods=['POST'], csrf=False)
	def get_report_maturity_receivable(self, **kw):
		if kw.get('company'):
			company = request.env['res.company'].sudo().search([('vat', '=', str(kw.get('company')))], limit=1)
			if not company:
				return {
					'status': 'error',
					'message': 'Falta la empresa.',      
				}
			if not kw.get('date_start') or not kw.get('date_end'):
				return {
				'status': 'error',
				'message': 'Faltan las fechas de inicio y fin.',        
			}

			date_start = kw.get('date_start')
			date_end = kw.get('date_end')
			date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
			date_end = datetime.strptime(date_end, '%Y-%m-%d').date()
			query = """
					SELECT row_number() OVER () AS id,
						fecha_emi, fecha_ven, cuenta, divisa, tdp, 
						doc_partner, partner, td_sunat, nro_comprobante, 
						saldo_mn, saldo_me, cero_treinta, treinta1_sesenta, 
						sesenta1_noventa, noventa1_ciento20, ciento21_ciento50, 
						ciento51_ciento80, ciento81_mas
						FROM get_maturity_analysis('%s','%s',%s,'%s')
				"""% (date_start, date_end,company.id, 'receivable')
			request.env.cr.execute(query)
			columns = [desc[0] for desc in request.env.cr.description]
			rows = request.env.cr.fetchall()
			result = [dict(zip(columns, row)) for row in rows]

			return {
                'status': 'success',
                'message': 'Datos enviados correctamente.',
                'columns': columns,
                'result': result,
            }