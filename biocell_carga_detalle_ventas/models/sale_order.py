# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class sale_order(models.Model):
    _inherit = "sale.order"
    
    def sh_import_sol(self):
        if self:
            action = self.env.ref('biocell_carga_detalle_ventas.sh_import_sol_action').read()[0]
            return action             
            
