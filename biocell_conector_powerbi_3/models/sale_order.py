from odoo import models, fields, api
from datetime import datetime,timedelta
class SaleOrder(models.Model):
    _inherit="sale.order"
    
    confirmation_date = fields.Datetime(
        string='Fecha de Confirmación'
    )
    
    def action_confirm(self):
        res = super().action_confirm()
        self.confirmation_date=(datetime.today() - timedelta(hours=5))
        return res