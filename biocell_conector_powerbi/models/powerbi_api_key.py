from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class PowerbiApiKey(models.Model):
    _name = 'powerbi.api.key'
    _description = 'Claves API PowerBI'
    
    name = fields.Char('Nombre')
    token = fields.Char('Token')