# -*- encoding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import Warning
import logging
log = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _prepare_despatch(self):
        res = super(StockPicking, self)._prepare_despatch()
        picking = self
        if picking.picking_type_id.code=='internal':
            res['delivery_address_id'] = False
        return res