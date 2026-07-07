# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from requests.exceptions import HTTPError
import requests
import logging
import pytz
_logger = logging.getLogger(__name__)



class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    segmento = fields.Selection([
        ('medicina_deportiva', 'Medicina Deportiva'),
        ('trauma', 'Trauma'),
        ('md_trauma', 'M.D / Trauma'),
        ('cmf', 'CMF')
    ], string='Segmento')
    
    tipo_cirugia = fields.Selection([
        ('cirugia', 'Cirugia'),
        ('cx_medavan', 'Cx Medavan'),
        ('consignacion', 'Consignacion'),
        ('venta_directa', 'Venta Directa'),
        ('oficina', 'Oficina'),
        ('cirugia_publica', 'Cirugia Pública'),
        ('infiltration','Cirugía Infiltración'),
        ('proceso', 'Proceso'),
        ('suspendida', 'Suspendida'),
        ('fundacion', 'Fundación'),
        ('cirugia_proceso_publico', 'Cirugia Proceso Publico'),
        ('cirugia_proceso_privado', 'Cirugia Proceso Privado'),
        ('taller', 'Taller'),
        ('licitacion', 'Licitacion'),
        ('donation', 'Donación'),
    ], string='Tipo de cirugía')
    
    articulacion_medicina_deportiva = fields.Selection([
        ('cadera', 'Cadera'),
        ('codo', 'Codo'),
        ('consignacion', 'Consignación'),
        ('consumibles', 'Consumibles'),
        ('distribuidor', 'Distribuidor'),
        ('equipos', 'Equipos'),
        ('hombro', 'Hombro'),
        ('licitacion', 'Licitacion'),
        ('mano_y_muneca', 'Mano_y_Muñeca'),
        ('oficina', 'Oficina'),
        ('pie_y_tobillo', 'Pie_y_Tobillo'),
        ('proceso', 'Proceso'),
        ('rodilla', 'Rodilla'),
        ('venta_directa', 'Venta_Directa'),
        ('otros', 'Otros')
    ], string='Articulación')
    
    articulacion_cmf = fields.Selection([
        ('oficina_cmf', 'OFICINA'),
        ('craneoplastia', 'CRANEOPLASTIA'),
        ('midface', 'MIDFACE'),
        ('ops', 'OPS'),
        ('ortognatica', 'ORTOGNATICA'),
        ('imf', 'IMF'),
        ('mandibula_trauma', 'MANDÍBULA_TRAUMA'),
        ('mandibula_reconstruccion', 'MANDÍBULA_RECONSTRUCCIÓN'),
        ('mentoplastia', 'MENTOPLASTIA')
    ], string='Articulación')
    
    kardex_instrumental = fields.Text(string='Kardex e instrumental')
    state_agendamiento = fields.Char(string='Estado Agendamiento', readonly=True, copy=False)
    codigo_agendamiento = fields.Char(string='Código de Agendamiento', readonly=True, copy=False)
    api_data_snapshot = fields.Text(string='Snapshot de datos API', readonly=True, copy=False, help='Datos guardados del último envío completo a la API')
    
    @api.onchange('segmento')
    def _onchange_segmento(self):
        """Limpiar los campos articulación cuando cambie el segmento"""
        self.articulacion_medicina_deportiva = False
        self.articulacion_cmf = False


    def generate_dev(self):
        response = super(SaleOrder, self).generate_dev()
        #api_response = self._send_to_api(self.state_agendamiento)		
        api_response = self._send_to_api('PROCESADO')
        self._handle_api_response(api_response, 'PROCESADO', 'Retorno Generado')
        return response
	
    # def write(self,vals):
    #     # Primero ejecutar el write original
    #     t = super().write(vals)
        
    #     # Segundo: verificar si es necesario enviar a la API
    #     for i in self:
    #         # NO enviar a la API si es aprobación de HC
    #         skip_api_for_hc = (
    #             hasattr(i, 'user_confirmación') and i.user_confirmación or  # Tiene usuario que aprobó HC
    #             hasattr(i, 'aprob_id') and i.aprob_id or                  # Tiene campo de aprobación
    #             hasattr(i, 'fecha_confirmación') and i.fecha_confirmación  # Tiene fecha de confirmación HC
    #         )
            
    #         if (i.state_agendamiento and
    #             'codigo_agendamiento' not in vals and
    #             'state_agendamiento' not in vals and
    #             'api_data_snapshot' not in vals and
    #             not skip_api_for_hc):  # No enviar si es aprobación HC
                
    #             try:
    #                 api_response = i._send_to_api(i.state_agendamiento)
                    
    #                 original_data = {
    #                     'order_lines_count': len(i.order_line),
    #                     'amount_total': i.amount_total,
    #                     'order_lines': [(line.product_id.id, line.product_uom_qty, line.price_unit) for line in i.order_line],
    #                 }
    #                 if not i._handle_api_response(api_response, i.state_agendamiento, 'Agendamiento Actualizada'):
    #                     # Si la API falla, solo registrar el error pero no bloquear el write
    #                     _logger.error(f"Error al enviar a API en pedido {i.name} desde write: Error de API")
    #                     i.message_post(
    #                         body='⚠️ <b>Error de API</b><br/>'
    #                              f'Error al enviar actualización a la API: Error de conexión<br/>'
    #                              'El pedido fue actualizado pero no se registró en el sistema CRM.',
    #                         message_type='notification'
    #                     )
    #             except Exception as api_error:
    #                 # Si hay excepción, solo registrar el error
    #                 _logger.error(f"Error al enviar a API en pedido {i.name} desde write: {str(api_error)}")
        
    #     return t
    
    def _build_api_payload(self, estado_agendamiento):
        """
        Método centralizado para construir el payload de la API
        Para estados PREPARADO y PROCESADO, reutiliza datos guardados de EN GESTION
        Para estados SIN GESTION y EN GESTION, construye payload completo
        """
        import json
        
        # Estados que deben reutilizar datos guardados
        estados_reutilizar_datos = ['PREPARADO', 'PROCESADO']
        
        """if estado_agendamiento in estados_reutilizar_datos:
            # Para PREPARADO y PROCESADO: reutilizar datos guardados de EN GESTION
            if self.api_data_snapshot:
                try:
                    # Recuperar datos guardados y solo cambiar el estado
                    saved_data = json.loads(self.api_data_snapshot)
                    saved_data['state_agendamiento'] = estado_agendamiento
                    # Envolver en estructura "data"
                    return {'data': saved_data}
                except (json.JSONDecodeError, KeyError) as e:
                    # Si hay error al recuperar datos, usar payload mínimo como fallback
                    data_payload = {
                        'sale_no': self.name,
                        'state_agendamiento': estado_agendamiento,
                    }
                    return {'data': data_payload}
            else:
                # Si no hay datos guardados, usar payload mínimo
                data_payload = {
                    'sale_no': self.name,
                    'state_agendamiento': estado_agendamiento,
                }
                return {'data': data_payload}
        """
        # Para SIN GESTION y EN GESTION: construir payload completo
        # Formatear la fecha de cirugía en GMT-5
        surgery_date = ""
        if hasattr(self, 'sugery_date') and self.sugery_date:
            timezone = pytz.timezone('America/Lima')
            if self.sugery_date.tzinfo is None:
                fecha_utc = pytz.utc.localize(self.sugery_date)
                fecha_agendada = fecha_utc.astimezone(timezone)
            else:
                fecha_agendada = self.sugery_date.astimezone(timezone)
            surgery_date = fecha_agendada.strftime("%Y-%m-%d %H:%M:%S")
        
        # Obtener la articulación seleccionada según el segmento
        articulacion_valor = ''
        if self.segmento == 'medicina_deportiva':
            articulation_selection = self._fields['articulacion_medicina_deportiva'].selection
            articulacion_valor = dict(articulation_selection).get(self.articulacion_medicina_deportiva, '')
        elif self.segmento == 'cmf':
            articulation_selection = self._fields['articulacion_cmf'].selection
            articulacion_valor = dict(articulation_selection).get(self.articulacion_cmf, '')
        
        # Construir el payload completo
        statusinvoice = {
            'upselling': 'Oportunidad de upselling',
            'invoiced': 'Facturado',
            'to invoice': 'A facturar',
            'no': 'Nada que facturar'}
        data_payload = {
            'sale_no': self.name,
            'establishment': self.shop_id.name if self.shop_id else '',
            'quoted_amount': self.amount_total,
            'client_name': self.partner_id.vat if self.partner_id and self.partner_id.vat else '',
            'doctor_name': self.name_doctor.name if self.name_doctor else '',
            'medical_center_name': self.medic_center.vat if self.medic_center and self.medic_center.vat else '',
            'surgery_date': surgery_date,
            'clinical_procedure': self.procedure_clinic_id.name if self.procedure_clinic_id else '',
            'state': self.state,
            'state_agendamiento': estado_agendamiento,
            'segmento': dict(self._fields['segmento'].selection).get(self.segmento, ''),
            'tipo_cirugia': dict(self._fields['tipo_cirugia'].selection).get(self.tipo_cirugia, ''),
            'articulacion': articulacion_valor,
            'invoice_ref': self.invoice_ids[0].name if self.invoice_ids else None,
            'invoice_amount': self.invoice_ids[0].amount_total if self.invoice_ids else None,
            'observations': self.kardex_instrumental if self.kardex_instrumental else '',
            'saleman_assigned': self.seller_id.name if self.seller_id else '',
            'paciente_c': self.name_patient,
            'estado_factura_c': statusinvoice[self.invoice_status],
            'created_by': self.create_uid.partner_id.name,
            'centro_medico': self.medic_center.name,
            'instrumentista':self.instrumentalist.name,
            'request_date':self.request_date.strftime('%Y-%m-%d %H:%M:%S') if self.request_date else None,
            'schedulling_request_date':self.schedulling_request_date.strftime('%Y-%m-%d %H:%M:%S') if self.schedulling_request_date else None,
        }
        
        # Guardar snapshot de datos para estados futuros (solo para EN GESTION)
        if estado_agendamiento == 'EN GESTION':
            import json
            self.api_data_snapshot = json.dumps(data_payload)
        
        # Envolver en estructura "data"
        return {'data': data_payload}
    
    def _handle_api_response(self, api_response, estado_agendamiento, action_name, extra_info=""):
        """
        Método centralizado para manejar respuestas de la API
        Unifica el manejo de éxito/error en todos los métodos
        """
        if api_response and api_response.get('success'):
            # ✅ API EXITOSA
            self.state_agendamiento = estado_agendamiento
            
            codigo_agendamiento = api_response.get('result', {}).get('codigo_agendamiento', 'Sin código')
            if hasattr(self, 'codigo_agendamiento'):
                self.codigo_agendamiento = codigo_agendamiento
            
            # Registrar éxito en el chat
            self.message_post(
                body=_('✅ <b>{}</b><br/>'
                      'Estado de agendamiento: <b>{}</b><br/>'
                      'Código de agendamiento: <b>{}</b><br/>'
                      '{}'
                      'Procesado por: {}').format(
                          action_name,
                          estado_agendamiento,
                          codigo_agendamiento,
                          extra_info,
                          self.env.user.name
                      ),
                message_type='notification'
            )
            return True
            
        else:
            # ❌ API FALLÓ
            error_message = api_response.get('message', 'Error desconocido en la API') if api_response else 'Error de conexión con la API'
            
            # Registrar error en el chat
            self.message_post(
                body=_('❌ <b>Error en {}</b><br/>'
                      'Error de API: <b>{}</b><br/>'
                      'Estado: <b>{}</b> (sin cambios)<br/>'
                      'Puede intentar nuevamente.<br/>'
                      'Intentado por: {}').format(
                          action_name,
                          error_message,
                          self.state_agendamiento or 'Sin estado',
                          self.env.user.name
                      ),
                message_type='notification'
            )
            return False
    
    def action_confirm(self):
        """
        Sobrescribir el método action_confirm para cambiar el estado de agendamiento y enviar a API
        IMPORTANTE: Solo envía a la API si previamente se agendó (se hizo clic en el botón AGENDAR)
        EVITA DUPLICACIONES: No envía a la API si es aprobación de HC
        """
        try:
            # PRIMERO: Permitir que otros módulos procesen normalmente
            result = super(SaleOrder, self).action_confirm()
            
            # SEGUNDO: Enviar a API después de la confirmación normal, SOLO si es apropiado
            for order in self:
                # NO enviar a la API si el pedido tiene campos de aprobación HC
                # Esto indica que viene del proceso de aprobación de HC
                skip_api_for_hc = (
                    hasattr(order, 'user_confirmación') or  # Tiene usuario que aprobó HC
                    hasattr(order, 'aprob_id') or          # Tiene campo de aprobación
                    hasattr(order, 'fecha_confirmación')   # Tiene fecha de confirmación HC
                )
                
                # if (not skip_api_for_hc and
                if (order.state in ('sale', 'done') and  # Ya está confirmado
                    hasattr(order, 'state_agendamiento') and
                    order.state_agendamiento in ['SIN GESTION', 'EN GESTION']):
                    
                    try:
                        # Capturar datos ORIGINALES
                        original_data = {
                            'order_lines_count': len(order.order_line),
                            'amount_total': order.amount_total,
                            'order_lines': [(line.product_id.id, line.product_uom_qty, line.price_unit) for line in order.order_line],
                        }
                        
                        # Enviar a API (esto es asíncrono, no bloquea la confirmación)
                        api_response = order._send_to_api('EN GESTION')
                        
                        # Manejar respuesta pero no fallar si hay error de API
                        order._handle_api_response(api_response, 'EN GESTION', 'Orden Confirmada')
                        
                    except Exception as api_error:
                        # Si la API falla, solo registrar el error pero NO mostrar error al usuario
                        _logger.error(f"Error al enviar a API en pedido {order.name}: {str(api_error)}")
                        order.message_post(
                            body='⚠️ <b>Error de API</b><br/>'
                                 f'Error al enviar pedido a la API: {str(api_error)}<br/>'
                                 'El pedido fue confirmado pero no se registró en el sistema CRM.',
                            message_type='notification'
                        )
                        # IMPORTANTE: No relanzar el error para no bloquear la confirmación
            
            return result
            
        except Exception as e:
            # Si hay error de otros módulos, intentar con super()
            return super(SaleOrder, self).action_confirm()
    
    def _send_to_api(self, estado_agendamiento):
        """
        Método auxiliar para enviar datos a la API
        """
            # # # # # # # PRODUCCION
            # 'Authorization': 'g4hK7a2zD9wX'
            # # # # # # # PRUEBAS
            # 'Authorization': 'M7tq4aZbP1yH'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'M7tq4aZbP1yH'
        }
        
        # Construir payload usando método centralizado
        payload = self._build_api_payload(estado_agendamiento)

        # --- INTEGRACIÓN API CRM ---
        try:
            # Determinar si es una creación o actualización
            if estado_agendamiento == 'SIN GESTION' and not self.codigo_agendamiento:
                # Crear nuevo agendamiento (única vez que se usa este endpoint)
                url = 'https://apisurgicalperuvisitas.saes-ec.com/api/agendamiento'
                # url = 'http://apisurgicalperuvisitas.saes-ec.com/api/agendamiento'
                response = requests.post(url, json=payload, headers=headers,verify=False)
            else:
                # Actualizar estado de agendamiento existente para todos los demás estados
                if self.codigo_agendamiento:
                    url = f'https://apisurgicalperuvisitas.saes-ec.com/api/agendamiento?codigo_agendamiento={self.codigo_agendamiento}'
                    # url = f'http://apisurgicalperuvisitas.saes-ec.com/api/agendamiento?codigo_agendamiento={self.codigo_agendamiento}'
                    response = requests.post(url, json=payload, headers=headers,verify=False)
                else:
                    return {
                        'success': False,
                        'codigo': 400,
                        'message': 'No se encontró código de agendamiento para actualizar',
                        'result': {}
                    }
            
            response.raise_for_status()  # Lanza una excepción si el código de status es 4xx/5xx
            response_data = response.json()

            # Siempre devolver la respuesta completa (éxito o error)
            if response_data.get('success'):
                # Actualizar el código de agendamiento si es una creación (cualquier estado inicial sin código)
                if not self.codigo_agendamiento and response_data.get('result', {}).get('codigo_agendamiento'):
                    codigo_agendamiento = response_data.get('result', {}).get('codigo_agendamiento')
                    if codigo_agendamiento and hasattr(self, 'codigo_agendamiento'):
                        self.codigo_agendamiento = codigo_agendamiento
                    _logger.info(f"Agendamiento creado exitosamente - Código: {codigo_agendamiento}")
                else:
                    _logger.info(f"Estado de agendamiento actualizado exitosamente - Código: {self.codigo_agendamiento}")
            else:
                _logger.error(f"Error al enviar a API: {response_data.get('message', 'Sin mensaje de error')}")

            return response_data  # Devolver toda la respuesta (éxito o error)

        except HTTPError as http_err:
            _logger.error(f"HTTP error occurred: {http_err}")
            return {
                'success': False,
                'codigo': response.status_code if 'response' in locals() else 500,
                'message': f'Error de conexión: {str(http_err)}',
                'result': {}
            }
        except Exception as err:
            _logger.error(f"An error occurred: {err}")
            return {
                'success': False,
                'codigo': 500,
                'message': f'Error inesperado: {str(err)}',
                'result': {}
            }
        # --- FIN INTEGRACIÓN API CRM ---
    
    def action_agendar(self):
        """
        Método para el botón AGENDAR
        """
        # Verificar si ya está agendado (tiene cualquier estado)
        #if self.state_agendamiento:
        #    # Solo registrar en el chat, sin notificación
        #    self.message_post(
        #        body=_('⚠️ <b>Intento de Agendamiento Duplicado</b><br/>'
        #              'Esta cotización ya ha sido agendada con estado: <b>{}</b>').format(self.state_agendamiento),
        #        message_type='notification'
        #    )
        #    return True

        # Asignar estado SIN GESTION antes de llamar a la API
        self.state_agendamiento = self.state_agendamiento or 'SIN GESTION'

        # Enviar a API
        api_response = self._send_to_api(self.state_agendamiento)

        # Manejar respuesta de la API de forma consistente
        if self._handle_api_response(api_response, self.state_agendamiento, 'Presupuesto Agendado'):
            return True
        else:
            # Si la API falla, mantener el estado SIN GESTION para permitir reintento
            return True

    def action_actualizar_agenda(self):
        """
        Método para el botón ACTUALIZAR AGENDA
        Reenvía a la API el estado actual de agendamiento sin modificarlo.
        """
        # Mantener el estado de agendamiento actual; si por alguna razón no lo tuviera, fijar SIN GESTION
        self.state_agendamiento = self.state_agendamiento or 'SIN GESTION'

        # Enviar a API
        api_response = self._send_to_api(self.state_agendamiento)

        # Manejar respuesta de la API
        self._handle_api_response(api_response, self.state_agendamiento, 'Agenda Actualizada')
        return True
    
    def generate_deva(self):
        """
        Herencia del método generate_dev del módulo biocell_devoluciones_comerciales_stock
        para actualizar el estado de agendamiento a PROCESADO y enviar a la API
        IMPORTANTE: Solo envía a la API si previamente se agendó (tiene state_agendamiento)
        """
        # Verificar que el método padre existe (compatibilidad con biocell_devoluciones_comerciales_stock)
        if not hasattr(super(SaleOrder, self), 'generate_dev'):
            raise UserError(_("❌ El módulo biocell_devoluciones_comerciales_stock no está disponible o no tiene el método generate_dev"))
        
        # PRIMERO: Validaciones básicas con verificaciones defensivas
        if hasattr(self, 'generado') and self.generado:
            raise UserError('Ya se genero el retorno')
        if hasattr(self, 'user_confirmación') and not self.user_confirmación.id:
            raise UserError('No se encuentra aprobado la HC')
        
        try:
            # SEGUNDO: Enviar a API SOLO si fue agendado previamente (tiene cualquier state_agendamiento)
            # NUEVA LÓGICA: Solo procesar si ya fue agendado anteriormente
            if hasattr(self, 'state_agendamiento') and self.state_agendamiento:
                api_response = self._send_to_api('PROCESADO')
                if not self._handle_api_response(api_response, 'PROCESADO', 'Retorno Generado'):
                    self.message_post(body = _("❌ No se pudo procesar el retorno: Error en la API.\n\n"
                                    "El retorno no se generará hasta que la API responda correctamente.\n"
                                    "Por favor, intente nuevamente."))
                    # raise UserError(_("❌ No se pudo procesar el retorno: Error en la API.\n\n"
                    #                 "El retorno no se generará hasta que la API responda correctamente.\n"
                    #                 "Por favor, intente nuevamente."))
            # Si no tiene state_agendamiento o está vacío, significa que no fue agendado,
            # por lo tanto NO enviar a la API y continuar con el proceso normal
            
            # TERCERO: Generar retorno directamente
            result = super(SaleOrder, self).generate_dev()
            return result
            
        except Exception as e:
            if 'API' in str(e) or 'retorno' in str(e):
                # Si es error de nuestro módulo, re-lanzar
                raise e
            else:
                # Si es error de otro módulo, intentar continuar
                return super(SaleOrder, self).generate_dev()
    
    def action_forzar_sincronizacion(self):
        """
        Método para forzar la sincronización manual de estados con la API
        Se usa cuando las órdenes quedaron atrapadas en 'SIN GESTION'
        """
        # Determinar el estado correcto según el estado de la orden
        if self.state == 'sale':
            nuevo_estado = 'EN GESTION'
        elif self.state == 'done':
            nuevo_estado = 'PROCESADO'
        else:
            nuevo_estado = self.state_agendamiento  # Mantener estado actual
        
        # Intentar enviar a la API
        try:
            api_response = self._send_to_api(nuevo_estado)
            
            if self._handle_api_response(api_response, nuevo_estado, 'Sincronización Forzada'):
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Sincronización Exitosa',
                        'message': f'Orden {self.name} sincronizada con estado {nuevo_estado}',
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Error de Sincronización',
                        'message': 'No se pudo sincronizar con la API. Intente nuevamente.',
                        'type': 'danger',
                        'sticky': True,
                    }
                }
                
        except Exception as e:
            _logger.error(f"Error en sincronización forzada de {self.name}: {str(e)}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error de Sincronización',
                    'message': f'Error: {str(e)}',
                    'type': 'danger',
                    'sticky': True,
                }
            }
