from odoo import models,fields

class SaleOrderLine(models.Model):
    _inherit="sale.order.line"
    
    order_label=fields.Char(
        related='order_id.name',
        string="Nombre de Orden de Venta"
    )
    order_user_id=fields.Many2one(
        'res.users',
        related='order_id.user_id',
        string="Vendedor de la Orden"
    )
    order_create_uid=fields.Many2one(
        'res.users',
        related='order_id.create_uid',
        string="Orden Creada Por"
    )