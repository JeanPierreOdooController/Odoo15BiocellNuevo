
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import datetime

class account_move(models.Model):
	_inherit = 'account.move'

	@api.model
	def create(self, vals):
		t = super(account_move, self).create(vals)
		t.origen_gt_replace()
		return t



	def origen_gt_replace(self):
		if self.env.company.origen_nro_compra != False:
			for i in self:
				i.l10n_pe_dte_service_order = i.purchase_ebill if i.purchase_ebill else False


class sale_order(models.Model):
	_inherit = 'sale.order'

	
	def write(self, vals):
		t = super(sale_order, self).write(vals)
		if "client_order_ref" in vals:
			for i in self:
				i.account_origen_gt_replace()
		return t

	def account_origen_gt_replace(self):
		for i in self:
			for fact in i.invoice_ids:
				fact.origen_gt_replace()