from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    block_transfers = fields.Boolean(
        string="Bloquear transferencias",
    )
