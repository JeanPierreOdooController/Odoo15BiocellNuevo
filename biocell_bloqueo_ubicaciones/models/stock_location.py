# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockLocation(models.Model):
    _inherit = 'stock.location'

    bloquea_grupo = fields.Boolean(
        string='Bloquea al Grupo',
        help='Si está marcado, los miembros del grupo "Restricción Cambios de Lote" '
             'no podrán crear, eliminar ni editar pickings que tengan esta ubicación '
             'como origen o destino.',
        default=False
    )

