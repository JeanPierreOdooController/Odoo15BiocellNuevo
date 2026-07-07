from odoo import models, api
from odoo.exceptions import UserError

class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    def write(self, vals):
        if self.env.user.has_group('biocell_bloqueos_comerciales_contactos.group_commercial_restricted'):
            if 'active' in vals:
                mensaje = 'No tiene permiso para archivar' if not vals['active'] else 'No tiene permiso para desarchivar'
                raise UserError(mensaje)
        return super(SaleOrderTemplate, self).write(vals)

    def unlink(self):
        if self.env.user.has_group('biocell_bloqueos_comerciales_contactos.group_commercial_restricted'):
            raise UserError('No tiene permiso para eliminar')
        return super(SaleOrderTemplate, self).unlink()