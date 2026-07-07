from odoo import models, api
from odoo.exceptions import AccessError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Usuario y ubicaciones permitidas (solo cambias aquí)
    RESTRICTED_USER_ID = 323  # Andres Rivadeneira
    ALLOWED_LOCATIONS = [151, 330, 149, 152, 150]
    ALLOWED_PICKING_TYPE = [
        321, 322, 325, 326, 327, 331, 328, 332, 333, 337,
        334, 338, 339, 343, 340, 344, 345, 349, 346, 350,
        351, 355, 352, 356
    ]  # ID(s) de tipo(s) de operación permitido(s)

    @api.onchange('location_id')
    def _onchange_location_id(self):
        if self.env.user.id == self.RESTRICTED_USER_ID:
            return {
                'domain': {
                    'location_id': [('id', 'in', self.ALLOWED_LOCATIONS)]
                }
            }

    @api.onchange('location_dest_id')
    def _onchange_location_dest_id(self):
        if self.env.user.id == self.RESTRICTED_USER_ID:
            return {
                'domain': {
                    'location_dest_id': [('id', 'in', self.ALLOWED_LOCATIONS)]
                }
            }

    @api.onchange('picking_type_id')
    def _onchange_picking_type_id(self):
        if self.env.user.id == self.RESTRICTED_USER_ID:
            return {
                'domain': {
                    'picking_type_id': [('id', 'in', self.ALLOWED_PICKING_TYPE)]
                }
            }

    @api.model
    def create(self, vals):
        if self.env.uid == self.RESTRICTED_USER_ID:
            location_id = vals.get('location_id')
            location_dest_id = vals.get('location_dest_id')
            picking_type_id = vals.get('picking_type_id')

            if location_id and location_id not in self.ALLOWED_LOCATIONS:
                raise AccessError(
                    "No tienes permiso para usar esta ubicación de origen, solo puede usar Educación Médica"
                )
            if location_dest_id and location_dest_id not in self.ALLOWED_LOCATIONS:
                raise AccessError(
                    "No tienes permiso para usar esta ubicación de destino, solo puede usar Educación Médica"
                )
            if picking_type_id and picking_type_id not in self.ALLOWED_PICKING_TYPE:
                raise AccessError(
                    "No tienes permiso para usar este tipo de operación"
                )

        return super().create(vals)

    def write(self, vals):
        if self.env.uid == self.RESTRICTED_USER_ID:
            location_id = vals.get('location_id')
            location_dest_id = vals.get('location_dest_id')
            picking_type_id = vals.get('picking_type_id')

            if location_id and location_id not in self.ALLOWED_LOCATIONS:
                raise AccessError(
                    "No tienes permiso para usar esta ubicación de origen, solo puede usar Educación Médica"
                )
            if location_dest_id and location_dest_id not in self.ALLOWED_LOCATIONS:
                raise AccessError(
                    "No tienes permiso para usar esta ubicación de destino, solo puede usar Educación Médica"
                )
            if picking_type_id and picking_type_id not in self.ALLOWED_PICKING_TYPE:
                raise AccessError(
                    "No tienes permiso para usar este tipo de operación"
                )

        return super().write(vals)
