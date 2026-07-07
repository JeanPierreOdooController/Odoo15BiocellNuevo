# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from requests.exceptions import HTTPError
import requests
import logging
import pytz
_logger = logging.getLogger(__name__)
import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    fecha_agendamiento = fields.Datetime('Fecha de Agendamiento')
    fecha_actualizacion_agendamiento = fields.Datetime('Fecha de Actualización de Agendamiento')
    fecha_consumo = fields.Datetime('Fecha de Consumo')

    def action_agendar(self):
        # Detectar si es primer agendamiento (state_agendamiento aún vacío)
        # ANTES de que super() lo llene con SIN GESTION
        es_primer_agendamiento = {i.id: not bool(i.state_agendamiento) for i in self}
        t = super(SaleOrder, self).action_agendar()
        ahora = datetime.datetime.now()
        for i in self:
            if es_primer_agendamiento.get(i.id):
                i.fecha_agendamiento = ahora
            else:
                i.fecha_actualizacion_agendamiento = ahora
        return t

    def action_actualizar_agenda(self):
        t = super(SaleOrder, self).action_actualizar_agenda()
        ahora = datetime.datetime.now()
        for i in self:
            i.fecha_actualizacion_agendamiento = ahora
        return t


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    fecha_agendamiento = fields.Datetime('Fecha de Agendamiento',related='order_id.fecha_agendamiento')
    fecha_actualizacion_agendamiento = fields.Datetime('Fecha de Actualización de Agendamiento',related='order_id.fecha_actualizacion_agendamiento')
    fecha_consumo = fields.Datetime('Fecha de Consumo',related='order_id.fecha_consumo')


class SaleOrderLineOrigin(models.Model):
    _inherit = 'sale.order.line.origin'

    fecha_agendamiento = fields.Datetime('Fecha de Agendamiento',related='order_id.fecha_agendamiento')
    fecha_actualizacion_agendamiento = fields.Datetime('Fecha de Actualización de Agendamiento',related='order_id.fecha_actualizacion_agendamiento')
    fecha_consumo = fields.Datetime('Fecha de Consumo',related='order_id.fecha_consumo')



class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def write(self,vals):
        for i in self:
            ant = i.qty_consumida
            super(StockMoveLine,i).write(vals)
            if ant != i.qty_consumida:
                i.move_id.sale_line_id.order_id.fecha_consumo = datetime.datetime.now()
