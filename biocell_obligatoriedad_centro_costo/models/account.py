# -*- coding: utf-8 -*-
# © 2011-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import _, api, exceptions, fields, models
from odoo.tools import float_is_zero
from odoo.exceptions import UserError


class AccountAccountType(models.Model):
	_inherit = "account.account.type"

	analytic_policy = fields.Selection(
		selection=[('optional', 'Opcional'),
				   ('always', 'Siempre'),
				   ('never', 'Nunca')],
		string=u'Política para las cuentas analíticas',
		required=True,
		default='optional',
		help="Set the policy for analytic accounts : if you select "
			 "'Optional', the accountant is free to put an analytic account "
			 "on an account move line with this type of account ; if you "
			 "select 'Always', the accountant will get an error message if "
			 "there is no analytic account ; if you select 'Never', the "
			 "accountant will get an error message if an analytic account "
			 "is present.")


class AccountMoveLine(models.Model):
	_inherit = "account.move.line"

	@api.model
	def _get_analytic_policy(self, account):
		""" Extension point to obtain analytic policy for an account """
		return account.user_type_id.analytic_policy

	def _check_analytic_required_msg(self):
		for move_line in self:
			prec = move_line.move_id.company_id.currency_id.rounding
			if (float_is_zero(move_line.debit, precision_rounding=prec) and
					float_is_zero(move_line.credit, precision_rounding=prec)):
				continue
			analytic_policy = self._get_analytic_policy(move_line.account_id)
			if (analytic_policy == 'always' and
					not move_line.analytic_account_id):
				return _(u"La política analítica está configurada en 'Siempre' con la cuenta "
						 "%s '%s' pero falta la cuenta analítica en la línea de movimiento de cuenta con la etiqueta '%s'."
						 ) % (move_line.account_id.code,
							  move_line.account_id.name,
							  move_line.name)
			elif (analytic_policy == 'never' and
					move_line.analytic_account_id):
				return _("La política analítica se establece en 'Nunca' con la cuenta %s "
						 "'%s' pero la línea de movimiento de cuenta con la etiqueta '%s' "
						 "tiene una cuenta analítica '%s'."
						 ) % (move_line.account_id.code,
							  move_line.account_id.name,
							  move_line.name,
							  move_line.analytic_account_id.name_get()[0][1])

	@api.constrains('analytic_account_id', 'account_id', 'debit', 'credit')
	def _check_analytic_required(self):
		for rec in self:
			message = rec._check_analytic_required_msg()
			if message:
				raise UserError(message)
