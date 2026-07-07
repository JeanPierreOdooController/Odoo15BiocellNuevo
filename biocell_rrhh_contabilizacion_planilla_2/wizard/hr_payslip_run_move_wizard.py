# -*- coding:utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import *
import base64

class HrPayslipRunMoveWizard(models.TransientModel):
	_inherit = 'hr.payslip.run.move.wizard'

	def generate_move(self):
		MainParameter = self.env['hr.main.parameter'].get_main_parameter()
		if not MainParameter.type_doc_pla.id:
			raise UserError('No se ha configurado el tipo de comprobante para Planilla')
		if not MainParameter.partner_id.id:
			raise UserError('No se ha configurado un partner para Planilla')
		PR = self.env['hr.payslip.run'].browse(self._context.get('payslip_run_id'))
		extra_line = {}
		if self.debit > self.credit:
			extra_line = {
				'account_id': self.account_id.id,
				'debit': 0,
				'credit': self.difference,
				'type_document_id': MainParameter.type_doc_pla.id,
				'nro_comp': 'PLAN-' + (PR.name.code).replace("-", ""),
				'name': 'Ajuste por Redondeo',
				'partner_id': MainParameter.partner_id.id}
		if self.credit > self.debit:
			extra_line = {
				'account_id': self.account_id.id,
				'debit': self.difference,
				'credit': 0,
				'type_document_id': MainParameter.type_doc_pla.id,
				'nro_comp': 'PLAN-' + (PR.name.code).replace("-", ""),
				'name': 'Ajuste por Redondeo',
				'partner_id': MainParameter.partner_id.id}

		lines = self.env['hr.payslip.run.move'].search([])
		# print("lines",lines)
		extra_line = [(0, 0, extra_line)] if extra_line else []
		move = self.env['account.move'].create({
			'journal_id': self.journal_id.id,
			'date': PR.date_end,
			'ref': 'PLAN-' + (PR.name.code).replace("-", ""),
			'line_ids': extra_line + [
				(0, 0, {
					'account_id': line.account_id.id,
					'debit': line.debit,
					'credit': line.credit,
					'type_document_id': MainParameter.type_doc_pla.id,
					'nro_comp': 'PLAN-' + (PR.name.code).replace("-", ""),
					'name': line['description'] if line['description'] else None,
					'analytic_account_id': line['analytic_account_id'].id if line['analytic_account_id'].id else None,
					'partner_id': line['partner_id'].id if line['partner_id'].id else MainParameter.partner_id.id,
				}) for line in lines
			]
		})
		move.action_post()
		PR.account_move_id = move.id
		PR.state = 'close'
		PR.slip_ids.action_payslip_hecho()
		return self.env['popup.it'].get_message('Generacion de Asiento Exitosa')


