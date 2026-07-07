# -*- enconding:utf-8 -*-
from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit="sale.order"
    
    clinical_delivery_id = fields.Many2one(
        'clinical.delivery.policy', 
        string='Política de Entrega',
        tracking=True
    )