from odoo import models, fields, api, _


class SaleOrderPowerBi(models.Model):
    _name="sale.order.powerbi"
    _description="PowerBi Ventas"
    _auto = False
    
    sale_order=fields.Char(
        string="Pedido de Venta"
    )
    
    product_code=fields.Char(
        string="Codigo Producto"
    )
    
    create_datetime=fields.Datetime(
        string="Fecha y Hora de Creación"
    )
    
    confirmation_datetime=fields.Datetime(
        string="Fecha y Hora de Confirmación de SO"
    )
    
    quotation_qty=fields.Float(
        string="Cantidad Cotización"
    )
    
    sent_qty=fields.Float(
        string="Cantidad Enviada"
    )
    
    consumed_qty=fields.Float(
        string="Cantidad Consumida"
    )    

    partner_id = fields.Char(
        string='Nombre Cliente'
    )
    
    saleperson_id = fields.Char(
        string='Asesor'
    )
    
    created_by_id = fields.Char(
        string='Creado Por'
    )
    # --------------------------------------
    plantilla_presupuesto_id = fields.Text(
        string='Plantillas de Presupuesto(Venta)'
    )
    
    plantilla_kardex_id = fields.Text(
        string='Plantillas de Kardex(Venta)'
    )
    
    plantilla_presupuesto_line_id = fields.Text(
        string='Plantilla de Presupuesto(origen)'
    )
    
    plantilla_kardex_line_id = fields.Text(
        string='Plantilla de Kardex(origen)'
    )

    medic_center = fields.Char(
        string='Centro Médico'
    )
    
    name_doctor = fields.Char(
        string='Nombre del Doctor'
    )
    
    sugery_date = fields.Datetime(
        string="Fecha/Hora Cirugía"
    )
    
    procedure_clinic_id = fields.Char(
        string='Procedimiento'
    )
    
    request_date = fields.Datetime(
        'Fecha de Solicitud de Cotización'
    )
    
    schedulling_request_date = fields.Datetime(
        'Fecha de Solicitud de Agendamiento'
    )