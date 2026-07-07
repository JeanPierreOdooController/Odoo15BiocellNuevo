from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    
    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        old_invoices= sale_orders.invoice_ids
        record=super(SaleAdvancePaymentInv,self).create_invoices()
        new_invoices= sale_orders.invoice_ids - old_invoices
        for invoice in new_invoices:
            related_sale=invoice.invoice_line_ids.sale_line_ids.order_id
            invoice.shop_id=related_sale.shop_id.id
        return record