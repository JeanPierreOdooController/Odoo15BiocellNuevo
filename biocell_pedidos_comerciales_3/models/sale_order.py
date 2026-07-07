# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    segmento = fields.Selection([
        ('medicina_deportiva', 'Medicina Deportiva'),
        ('trauma', 'Trauma'),
        ('md_trauma', 'M.D / Trauma'),
        ('cmf', 'CMF'),
        ('ortobiologico', 'Ortobiológico'),
    ], string='Segmento')

    @api.onchange('segmento')
    def _onchange_segmento_ortobiologico(self):
        """
        Medicina Deportiva y Ortobiológico
        usan la misma articulación
        """
        if self.segmento in ('medicina_deportiva', 'ortobiologico'):
            # Limpiar CMF
            self.articulacion_cmf = False
        else:
            # Si cambia a otro segmento, limpiar medicina deportiva
            self.articulacion_medicina_deportiva = False
