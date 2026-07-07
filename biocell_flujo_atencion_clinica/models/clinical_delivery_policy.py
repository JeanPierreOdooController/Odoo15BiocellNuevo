from odoo import models, fields, api, _

class ClinicalDeliveryPolicy(models.Model):
    _name="clinical.delivery.policy"
    _description="Politica de Entrega Clinica"
    
    name = fields.Char('Nombre')