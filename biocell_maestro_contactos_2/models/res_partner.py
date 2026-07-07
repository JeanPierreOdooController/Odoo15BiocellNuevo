from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    seller_id = fields.Many2one(
        'res.partner',
        string='Vendedor IT',
        domain=[('is_seller', '=', True)],
    )

    is_seller = fields.Boolean(
        string='Es Vendedor IT',
    )
