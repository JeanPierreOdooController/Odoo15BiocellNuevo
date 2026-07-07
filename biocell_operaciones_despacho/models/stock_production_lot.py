from odoo import models, fields

class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    block_transfers = fields.Boolean(
        string="Bloquear transferencias",
    )
