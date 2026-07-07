from odoo import models, api
from odoo.exceptions import UserError
class SaleOrder(models.Model):
    _inherit="sale.order"
    
    @api.model
    def create(self, vals):
        res=super().create(vals)
        order_lines=self.env['sale.order.line'].search([
            ('order_id','=',self.id)
        ])
        # Filter sale lines without sale_type
        order_lines=[order for order in order_lines if not order.sale_type]
        if not order_lines:
            return res
        for order in order_lines:
            order.sale_type='sale'
        return res
    
    def write(self, vals):
        res=super().write(vals)
        order_lines=self.env['sale.order.line'].search([
            ('order_id','=',self.id)
        ])
        # Filter sale lines without sale_type
        order_lines=[order for order in order_lines if not order.sale_type]
        if not order_lines:
            return res
        for order in order_lines:
            order.sale_type='sale'
        return res