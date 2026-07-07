# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date
from odoo.exceptions import UserError
import base64
from io import BytesIO
import re
import uuid


class AccountBookDiaryWizard(models.TransientModel):
	_inherit = 'account.book.diary.wizard'


	def _get_sql(self):
		sql_journals = ""
		if self.content == 'pick':
			if not self.journal_ids:
				raise UserError(u'Debe escoger por lo menos un Diario.')
			sql_journals = "WHERE am.journal_id in (%s) " % (','.join(str(i) for i in self.journal_ids.ids))

		sql = """SELECT
			vst1.periodo::character varying,vst1.fecha,vst1.libro,vst1.voucher,
			vst1.cuenta,vst1.debe,vst1.haber,vst1.balance,
			vst1.moneda,vst1.tc,vst1.importe_me,vst1.cta_analitica,
			regexp_replace(vst1.glosa, '[^a-zA-Z0-9-]', '', 'g') as glosa,
			vst1.td_partner,vst1.doc_partner,vst1.partner,
			vst1.td_sunat,vst1.nro_comprobante,vst1.fecha_doc,vst1.fecha_ven,
			vst1.col_reg,vst1.monto_reg,vst1.medio_pago,vst1.ple_diario,
			vst1.ple_compras,vst1.ple_ventas, aml.employee_id
			FROM get_diariog('%s','%s',%d) vst1
			LEFT JOIN account_move_line aml ON aml.id = vst1.move_line_id
			LEFT JOIN account_move am on am.id =  vst1.move_id %s
		""" % (self.date_from.strftime('%Y/%m/%d') if self.show_by == 'date' else self.period_from_id.date_start.strftime('%Y/%m/%d'),
			self.date_to.strftime('%Y/%m/%d') if self.show_by == 'date' else self.period_to_id.date_end.strftime('%Y/%m/%d'),
			self.company_id.id,
			sql_journals)
		return sql

	
	
	def get_header(self):
		HEADERS = ['PERIODO','FECHA','LIBRO','VOUCHER','CUENTA','DEBE','HABER','BALANCE','MON','TC','IMP ME',
		'CTA ANALITICA','GLOSA','TDP','RUC','PARTNER','TD','NRO COMP','FECHA DOC','FECHA VEN','COL REG','MONTO REG','MED PAGO',
		'PLE DIARIO','PLE COMPRAS','PLE VENTAS','EMPLEADO']
		return HEADERS