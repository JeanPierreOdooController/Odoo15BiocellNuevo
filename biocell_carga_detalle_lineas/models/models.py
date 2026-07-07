from odoo import models, fields, api, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.exceptions import UserError
import base64


class stock_picking(models.Model):
	_inherit = 'stock.picking'

	def importar_move_lines(self):
		ctx = {
			'default_stock_picking_id': self.id,
			'default_mensaje_formato': "PRODUCTO;LOTE;CANTIDAD;FECHA VENCIMIENTO;PRECIO",
						}
		return {
			'name': _('Importar Movimientos Almacen'),
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'target': 'new',
			'res_model': 'importador.moves.lines',
			'context': ctx,
			}
