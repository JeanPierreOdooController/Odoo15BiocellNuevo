from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    
    seller_id = fields.Many2one('res.partner', string='Vendedor IT', domain=[('is_seller', '=', True)], tracking=True)


    # @api.onchange('partner_id')
    # def _onchange_partner_id_set_seller(self):
    #     if self.partner_id and self.partner_id.seller_id:
    #         self.seller_id = self.partner_id.seller_id
    #     else:
    #         self.seller_id = False


    @api.model
    def create(self, vals):
        am = super(AccountMove, self).create(vals)
        am._seller_account_move_sale_order()
        return am

    def write(self,vals):
        am = super(AccountMove,self).write(vals)
        self._seller_account_move_sale_order()
        return am


    def _seller_account_move_sale_order(self):
        for am in self:
            if not am.seller_id and am.move_type == 'out_invoice':
                seller_ids = set()
                for aml in am.invoice_line_ids:
                    if aml.product_id and aml.sale_line_ids:
                        for sol in aml.sale_line_ids:
                            if sol.order_id.seller_id:
                                seller_ids.add(sol.order_id.seller_id.id)
                if len(seller_ids) > 1:
                    raise UserError("Existen múltiples vendedores asociados a esta factura.")
                elif len(seller_ids) == 1:
                    am.seller_id = list(seller_ids)[0]
                else:
                    pass


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    seller_id = fields.Many2one(
        'res.partner',
        string='Vendedor IT',
        domain=[('is_seller', '=', True)],
    )

    preparation_user_id = fields.Many2one(
        'res.users',
        string='Responsable de preparación IT',
        readonly=True,
    )

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if not order.preparation_user_id:
                order.preparation_user_id = self.env.user.id
        return res

    @api.onchange('partner_id')
    def _onchange_partner_id_set_seller(self):
        if self.partner_id and self.partner_id.seller_id:
            self.seller_id = self.partner_id.seller_id
        else:
            self.seller_id = False