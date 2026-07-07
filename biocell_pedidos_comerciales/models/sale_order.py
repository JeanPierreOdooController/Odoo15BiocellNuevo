# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    articulacion_trauma_md = fields.Selection([
        ('rodilla', 'Rodilla'),
        ('venta_directa', 'Venta Directa'),
        ('sistema_fibertape_cerclage', 'Sistema Fibertape Cerclage'),
        ('sistema_mini_cfs', 'Sistema Mini CFS'),
        ('sistema_placa_calcaneo', 'Sistema Placa Calcáneo'),
        ('sistema_placa_clavicula', 'Sistema Placa Clavícula'),
        ('sistema_placa_perone', 'Sistema Placa Peroné'),
        ('sistema_placa_proximal_humero', 'Sistema Placa Proximal Húmero'),
        ('sistema_placa_volar', 'Sistema Placa Volar'),
        ('sistema_tornillos_compresion_mediano', 'Sistema Tornillos Compresión Mediano'),
        ('sistema_tornillos_compresion_mini', 'Sistema Tornillos Compresión Mini'),
        ('sistema_fractura_distal_tibia', 'Sistema Fractura Distal de Tibia'),
        ('na', 'N.A.')
    ], string='Articulación')


    @api.onchange('segmento')
    def _onchange_segmento_ortobiologico(self):
        # Limpiar otras articulaciones
        if self.segmento in ('trauma', 'md_trauma'):
            self.articulacion_medicina_deportiva  = False
            self.articulacion_cmf   = False
        else:
            # Si cambia a otro segmento, limpiar articulacion traume
            self.articulacion_trauma_md  = False
