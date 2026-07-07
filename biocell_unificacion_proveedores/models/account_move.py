from odoo import _, api, fields, models, tools

class account_move(models.Model):

    _inherit = 'account.move'


    @api.constrains('name', 'partner_id', 'company_id', 'posted_before')
    def _biocell_unificacion_proveedores_number(self):
      return