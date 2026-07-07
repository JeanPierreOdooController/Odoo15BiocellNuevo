# -*- encoding: utf-8 -*-
from odoo import fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import Warning
import logging
log = logging.getLogger(__name__)

class StockMove(models.Model):
	_inherit = 'stock.move'

	def get_despatch_product_name(self):
		return self.description_picking if self.description_picking else self.product_id.display_name

class StockPicking(models.Model):
	_inherit = 'stock.picking'

	expedition_id = fields.Many2one('logistic.expedition', string='Expedition')
	despatch_id = fields.Many2one('logistic.despatch', string='Despatch', copy=False)

	def _prepare_despatch(self):
		picking = self
		partner_id = picking.partner_id.id
		delivery_address_id = picking.partner_id.id

		if picking.partner_id.parent_id:
			partner_id = picking.partner_id.parent_id.id
			delivery_address_id = picking.partner_id.parent_id.id

		if not picking.partner_id:
			delivery_address_id = picking.picking_type_id.warehouse_id.partner_id.id

		journal_id = self.env['account.journal'].search([('type','=','general'),('code','=like','T%')])
		if not journal_id:
			journal_id = self.env['account.journal'].search([('type','=','general')])

		if not journal_id:
			raise Warning('Journals not found for despatchs')

		origin_address_id = False
		delivery_address_id = False
		warehouse_id = False
		if picking.picking_type_id.code=='incoming':
			origin_address_id = picking.partner_id.id
			delivery_address_id = picking.picking_type_id.warehouse_id.partner_id.id
			warehouse_id = picking.picking_type_id.warehouse_id
		elif picking.picking_type_id.code=='outgoing':
			origin_address_id = picking.picking_type_id.warehouse_id.partner_id.id
			delivery_address_id = picking.partner_id.id
			warehouse_id = picking.picking_type_id.warehouse_id
		elif picking.picking_type_id.code=='internal':
			origin_address_id = picking.picking_type_id.warehouse_id.partner_id.id
			delivery_address_id = origin_address_id
			warehouse_id = picking.picking_type_id.warehouse_id
		despatch = {
			'warehouse_id': warehouse_id.id if warehouse_id else False,
			'journal_id': warehouse_id.despatch_journal_ids[0].id if warehouse_id.despatch_journal_ids else journal_id[0].id,
			'company_id':picking.company_id.id,
			'partner_id':partner_id,
			'origin_address_id':origin_address_id,
			'delivery_address_id':delivery_address_id,
			'line_ids':[],
			'picking_ids':[[6,0,[picking.id]]]
		}
		bio_nota = """<table width="100%" border="0" cellpadding="2" cellspacing="0">
			<colgroup>
				<col width="50%"/>
				<col width="50%"/>
			</colgroup>
			<tbody>
				<tr>
					<td style="vertical-align: top;">
						<strong>Código Cirugía: </strong>{codigo_cirugia}<br/>
						<strong>Fecha de Cirugía: </strong>{fecha_cirugia}<br/>
						<strong>Hora Cirugía: </strong>{hora_cirugia}<br/>
						<strong>Ciudad: </strong>{ciudad}<br/>
						<strong>Seguro Médico: </strong><br/>
						<strong>Nombre Paciente: </strong>{nombre_paciente}<br/>
						<strong>DNI/RUC Paciente: </strong>{dni_paciente}<br/>
					</td>
					<td style="vertical-align: top;">
						<strong>Tipo: </strong>{tipo}<br/>
						<strong>O.Com/EQC: </strong>{oc_com_eqc}<br/>
						<strong>No. Ingreso(HCL): </strong>ND<br/>
						<strong>Sede: </strong>{sede}<br/>
						<strong>Nombre Cirujano: </strong>{nombre_cirujano}<br/>
					</td>
				</tr>
			</tbody>
		</table>""".format(codigo_cirugia=picking.cod_cirugia or '',
							fecha_cirugia= (picking.sugery_date - timedelta(hours=5)).strftime("%d/%m/%Y") if picking.sugery_date else '',
							hora_cirugia= (picking.sugery_date - timedelta(hours=5)).strftime("%H:%M:%S") if picking.sugery_date else '',
							ciudad=picking.shop_id or '',
							nombre_paciente=picking.name_patient or '',
							dni_paciente=picking.patient_vat or '',
							tipo=picking.categoria_rel or '',
							#oc_com_eqc=self.picking_type_id.warehouse_id.partner_id.street,
							oc_com_eqc= (picking.picking_type_id.warehouse_id.partner_id.street_name or '') \
								+ (picking.picking_type_id.warehouse_id.partner_id.street_number and (' ' + picking.picking_type_id.warehouse_id.partner_id.street_number) or '') \
								+ (picking.picking_type_id.warehouse_id.partner_id.street_number2 and (' ' + picking.picking_type_id.warehouse_id.partner_id.street_number2) or '') \
								+ (picking.picking_type_id.warehouse_id.partner_id.street2 and (' ' + picking.picking_type_id.warehouse_id.partner_id.street2) or '') \
								+ (picking.picking_type_id.warehouse_id.partner_id.district_id and ', ' + picking.picking_type_id.warehouse_id.partner_id.district_id.name or '') \
								+ (picking.picking_type_id.warehouse_id.partner_id.city_id and ', ' + picking.picking_type_id.warehouse_id.partner_id.city_id.name or '') \
								+ (picking.picking_type_id.warehouse_id.partner_id.state_id and ', ' + picking.picking_type_id.warehouse_id.partner_id.state_id.name or '') \
								+ (picking.picking_type_id.warehouse_id.partner_id.country_id and ', ' + picking.picking_type_id.warehouse_id.partner_id.country_id.name or ''),
							sede=picking.medic_center or '',
							nombre_cirujano=picking.name_doctor or ''
							)
		despatch['bio_nota'] = bio_nota
		despatch['bio_vendedor'] = picking.user_id_sale.name if picking.user_id_sale else ''
		despatch['bio_payment_term'] = picking.payment_term_id or ''
		despatch['bio_nro_gaveta'] = picking.nro_gaveta or ''
		despatch['bio_name_sale'] = picking.name_sale or ''
		if picking.note:
			despatch['note'] = picking.note
		if self._context.get('force_issue_date', False):
			despatch['issue_date'] = self._context.get('force_issue_date')
		if self._context.get('force_start_date', False):
			despatch['start_date'] = self._context.get('force_start_date')
		if self._context.get('force_journal_id', False):
			despatch['journal_id'] = self._context.get('force_journal_id')
		if self._context.get('force_shipment_reason', False):
			despatch['shipment_reason'] = self._context.get('force_shipment_reason')
		if self._context.get('force_carrier_id', False):
			despatch['carrier_id'] = self._context.get('force_carrier_id')
		if self._context.get('force_vehicle_id', False):
			despatch['vehicle_id'] = self._context.get('force_vehicle_id')
		if self._context.get('force_driver_id', False):
			despatch['driver_id'] = self._context.get('force_driver_id')
		if self._context.get('force_origin_address_id', False):
			despatch['origin_address_id'] = self._context.get('force_origin_address_id')
		if self._context.get('force_delivery_address_id', False):
			despatch['delivery_address_id'] = self._context.get('force_delivery_address_id')
		if self._context.get('force_internal_number', False):
			despatch['internal_number'] = self._context.get('force_internal_number')
		
		weight_total = 0
		for line in picking.move_line_ids_without_package.filtered(lambda x:x.qty_done>0):
			'''if line.sale_line_id:
				product_name = line.sale_line_id.name'''
			despatch['line_ids'].append([0,0,{
				'product_id':line.product_id.id,
				'name':line.product_id.name,
				'quantity':line.qty_done,
				'uom_id':line.product_uom_id.id,
				'weight':line.product_id.weight*line.qty_done ,
				'volume': line.product_id.volume * line.qty_done,
				#'bio_cantidad': line.bio_cantidad,
				#'bio_descuento': line.bio_descuento,
				'bio_pu': line.move_id.bio_pu,
				'bio_total': line.move_id.bio_pu * line.qty_done,
				#'bio_categoria': line.tipo_product,
				'bio_lote':line.lot_id.name,
				'bio_fecven': (line.lot_id.expiration_date - timedelta(hours=5)).strftime('%d/%m/%Y') if line.lot_id.expiration_date else '',
				'bio_package_id': line.package_id.id,
				#'bio_lote':'',
				}])
		return despatch

	def generate_logistic_despatch(self):
		despatch_ids = []
		for picking in self:
			if picking.company_id.logistic_picking_done_restrict and picking.state!='done':
				raise Warning(_('Picking status is not done'))
			if picking.despatch_id:
				if picking.despatch_id.state=='open':
					raise Warning(_('This document already has a remission guide'))
			despatch = picking._prepare_despatch()
			_despatch = self.env['logistic.despatch'].create(despatch)
			picking.write({'despatch_id':_despatch.id})
			despatch_ids.append(_despatch.id)
		if self._context.get('force_return_array', False):
			return despatch_ids
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'logistic.despatch',
			'view_mode': 'form',
			'res_id': _despatch.id,
			'target': 'current',
			'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}}
		}
