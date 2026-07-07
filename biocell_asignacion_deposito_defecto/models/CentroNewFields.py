from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CentroNewField(models.Model):
    _inherit="account.analytic.journal"

    codigo=fields.Char(string="Codigo",size=2)
    almacen_predeterminado=fields.Many2one(
        "stock.warehouse",
        string="Almacen Predeterminado"
    )


class SaleWarehouse(models.Model):
    _inherit="sale.order"

    @api.onchange('shop_id','partner_id')
    def onchange_shop_id(self):
        for r in self:
            r.warehouse_id = r.shop_id.almacen_predeterminado.id

    # Sobrecarga de nativo 
    @api.onchange('user_id')
    def onchange_user_id(self):
        super().onchange_user_id()
        if not self.warehouse_id or self.warehouse_id != self.shop_id.almacen_predeterminado.id:
            self.warehouse_id = self.shop_id.almacen_predeterminado.id