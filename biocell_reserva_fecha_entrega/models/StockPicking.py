from odoo import models, api, fields
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit="stock.picking"
    
    commitment_date = fields.Datetime(
        compute='_compute_commitment_date_from_sale',
        string='Fecha de Entrega'
    )
    expected_date = fields.Date(
        compute='_compute_expected_date_from_sale',
        string='Fecha Prevista'
    )
    
    
    @api.depends('sale_id')
    def _compute_commitment_date_from_sale(self):
        for r in self:
            if not r.sale_id:
                r.commitment_date=False
            r.commitment_date=r.sale_id.commitment_date
            
    @api.depends('sale_id')
    def _compute_expected_date_from_sale(self):
        for r in self:
            if not r.sale_id:
                r.expected_date=False
            r.expected_date=r.sale_id.expected_date
        