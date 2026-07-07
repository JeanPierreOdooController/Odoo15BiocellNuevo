# -*- enconding:utf-8 -*-
from odoo import models, fields, api, _

class StockPicking(models.Model):
    _inherit="stock.picking"
    
    clinical_delivery_id = fields.Many2one(
        'clinical.delivery.policy', 
        string='Política de Entrega',
        compute="_compute_clinical_delivery_id"
    )
    
    @api.depends('sale_id')
    def _compute_clinical_delivery_id(self):
        for r in self:
            r.clinical_delivery_id=r.sale_id.clinical_delivery_id
        