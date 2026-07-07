# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    nro_cotizacion = fields.Char(
        string='Nro de Cotización',
        readonly=True,
        help='Número de la cotización que generó esta factura'
    )
    
    @api.model_create_multi
    def create(self, vals_list):
        """
        Sobrescribir el método create para agregar automáticamente el número de cotización
        cuando se crea una factura desde una orden de venta
        """
        try:
            for vals in vals_list:
                # Si la factura se crea desde una orden de venta
                if vals.get('invoice_origin'):
                    # Buscar la orden de venta por su nombre con validaciones adicionales
                    sale_order = self.env['sale.order'].search([
                        ('name', '=', vals['invoice_origin'])
                    ], limit=1)
                    
                    # Verificar que existe y tiene el campo name
                    if sale_order and hasattr(sale_order, 'name') and sale_order.name:
                        vals['nro_cotizacion'] = sale_order.name
                        
        except Exception as e:
            # Si hay error en nuestro código, no afectar la creación de la factura
            # Solo registrar el error en log
            import logging
            _logger = logging.getLogger(__name__)
            _logger.warning(f"Error en biocell_conector_ventas al crear account.move: {str(e)}")
        
        # SIEMPRE llamar super() para que otros módulos funcionen
        return super(AccountMove, self).create(vals_list)

    def l10n_pe_dte_action_send(self):
        for i in self:
            sale_order = self.env['sale.order'].search([
                        ('name', '=', self.nro_cotizacion)
                    ], limit=1)
            if sale_order:
                sale_order._send_to_api(sale_order.state_agendamiento)

        return super(AccountMove, self).l10n_pe_dte_action_send()
