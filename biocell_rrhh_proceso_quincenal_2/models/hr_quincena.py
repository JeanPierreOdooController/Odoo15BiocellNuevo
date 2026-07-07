# -*- coding:utf-8 -*-
import base64
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
from odoo.osv import osv, expression
import io
import datetime
from dateutil.relativedelta import relativedelta
from xlsxwriter.workbook import Workbook

class hr_quincenales(models.Model):
	_inherit = 'hr.quincenales'


	def generate(self):
		ReportBase = self.env['report.base']
		MainParameter = self.env['hr.main.parameter'].get_main_parameter()
		structure_type_id = self.env['hr.payroll.structure.type'].search([('default_schedule_pay', '=', 'monthly')],limit=1).id
		he = self.env['hr.employee'].search([('contract_ids.state', 'in', ('open', 'close')),('contract_ids.structure_type_id', '=', structure_type_id),
											 ('company_id', '=', self.env.company.id)])

		dateini = str(self.fecha.year) + '-' + str(self.fecha.month).rjust(2, '0') + '-01'
		nfecha = datetime.datetime.strptime(dateini, '%Y-%m-%d')
		contracts = he._get_contracts(nfecha, (self.fecha), states=['open', 'close'])
		# print("contracts",contracts)
		to_create = []
		for contrato in contracts:
			af = MainParameter.rmv * 0.1
			membership = contrato.membership_id
			onp = afp_jub = afp_si = afp_mixed_com = afp_fixed_com = 0
			sueldo = contrato.wage + (af if contrato.employee_id.children > 0 else 0)
			if MainParameter.compute_afiliacion:
				if membership.is_afp:
					afp_jub = ReportBase.custom_round(membership.retirement_fund / 100 * sueldo, 2)
					afp_si = ReportBase.custom_round(membership.prima_insurance / 100 * sueldo, 2)
					if contrato.commision_type=='flow':
						afp_fixed_com = ReportBase.custom_round(membership.fixed_commision / 100 * sueldo, 2)
					if contrato.commision_type=='mixed':
						afp_mixed_com = ReportBase.custom_round(membership.mixed_commision / 100 * sueldo, 2)
				else:
					onp = ReportBase.custom_round(membership.retirement_fund / 100 * sueldo, 2)
			quin_desc = 0
			vals = {
				'quincenal_id':self.id,
				'employee_id':contrato.employee_id.id,
				'contract_id':contrato.id,
				'codigo_trabajador':contrato.employee_id.identification_id,
				'nombres':contrato.employee_id.name,
				'fecha_ingreso':contrato.date_start,
				'basico':contrato.wage,
				'asignacion_familiar':af if (contrato.employee_id.children > 0 and MainParameter.compute_af) else 0,
				'onp':onp,
				'afp_com':afp_mixed_com + afp_fixed_com,
				'afp_prima':afp_si,
				'afp_jub':afp_jub,
				'quinta_cat':quin_desc}
			to_create.append(vals)

		for v in to_create:
			hql = self.env['hr.quincenales.lines'].search([('employee_id', '=', v['employee_id']), ('quincenal_id', '=', v['quincenal_id'])])
			if len(hql):
				hql[0].write(v)
			else:
				self.env['hr.quincenales.lines'].create(v)