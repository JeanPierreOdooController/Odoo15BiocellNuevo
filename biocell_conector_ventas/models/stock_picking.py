# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def generate_logistic_despatch(self):
        """
        Sobrescribir el método generate_logistic_despatch para enviar a API cuando se genere la guía
        IMPORTANTE: Solo envía a la API si previamente se agendó (tiene state_agendamiento)
        """
        # Llamar al método padre primero
        result = super(StockPicking, self).generate_logistic_despatch()
        
        # Enviar a API con estado "PREPARADO" para albaranes de salida e internos
        for picking in self:
            if picking.origin and picking.picking_type_code in ['outgoing', 'internal']:
                # Buscar la orden de venta relacionada
                sale_order = self.env['sale.order'].search([('name', '=', picking.origin)], limit=1)
                
                if sale_order:
                    # NUEVA LÓGICA: Solo procesar si ya fue agendado previamente (tiene state_agendamiento)
                    if hasattr(sale_order, 'state_agendamiento') and sale_order.state_agendamiento:
                        # VALIDACIÓN: Si ya está en estado PREPARADO, no volver a procesar
                        if sale_order.state_agendamiento == 'PREPARADO':
                            continue  # Continuar con el siguiente picking
                        
                        # ENVIAR A LA API (solo cambio de estado, no actualización de datos)
                        api_response = sale_order._send_to_api('PREPARADO')
                        
                        # VALIDAR RESPUESTA DE LA API
                        if api_response and api_response.get('success') == True:
                            # ✅ API EXITOSA - Cambiar estado a PREPARADO
                            sale_order.state_agendamiento = 'PREPARADO'
                            
                            codigo_agendamiento = api_response.get('result', {}).get('codigo_agendamiento', 'Sin código')
                            if hasattr(sale_order, 'codigo_agendamiento'):
                                sale_order.codigo_agendamiento = codigo_agendamiento
                            
                            # Registrar éxito en el chat
                            sale_order.message_post(
                                body=_('✅ <b>Guía Generada Exitosamente</b><br/>'
                                      'Estado de agendamiento: <b>PREPARADO</b><br/>'
                                      'Código de agendamiento: <b>{}</b><br/>'
                                      'Albarán: <b>{}</b><br/>'
                                      'Generado por: {}').format(
                                          codigo_agendamiento,
                                          picking.name,
                                          self.env.user.name
                                      ),
                                message_type='notification'
                            )
                            
                        else:
                            # ❌ API FALLÓ - NO cambiar estado, permitir reintento
                            error_message = api_response.get('message', 'Error desconocido en la API') if api_response else 'Error de conexión con la API'
                            
                            # Registrar error en el chat
                            sale_order.message_post(
                                body=_('❌ <b>Error al Generar Guía</b><br/>'
                                      'Error de API: <b>{}</b><br/>'
                                      'Estado: <b>{}</b> (sin cambios)<br/>'
                                      'Albarán: <b>{}</b><br/>'
                                      'Puede intentar nuevamente.<br/>'
                                      'Intentado por: {}').format(
                                          error_message,
                                          sale_order.state_agendamiento or 'Sin estado',
                                          picking.name,
                                          self.env.user.name
                                      ),
                                message_type='notification'
                            )
                    else:
                        # Si no tiene state_agendamiento o está vacío, no fue agendado
                        # NO enviar a la API, solo registrar guía generada normalmente
                        sale_order.message_post(
                            body=_('📦 <b>Guía Generada</b><br/>'
                                  'Albarán: <b>{}</b><br/>'
                                  'Generado por: {}<br/>'
                                  '<i>Nota: Esta orden no requiere gestión de agendamiento</i>').format(
                                      picking.name,
                                      self.env.user.name
                                  ),
                            message_type='notification'
                        )
        
        return result