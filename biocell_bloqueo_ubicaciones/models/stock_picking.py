# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _check_restricted_location(self, location_id=None, location_dest_id=None):
        if not self.env.user.has_group('biocell_bloqueo_ubicaciones.group_restriction_cambios_lote'):
            return False, None
        
        if location_id:
            if isinstance(location_id, int):
                location = self.env['stock.location'].browse(location_id)
            else:
                location = location_id
            if location and location.bloquea_grupo:
                return True, location
        
        if location_dest_id:
            if isinstance(location_dest_id, int):
                location_dest = self.env['stock.location'].browse(location_dest_id)
            else:
                location_dest = location_dest_id
            if location_dest and location_dest.bloquea_grupo:
                return True, location_dest
        
        if self.location_id and self.location_id.bloquea_grupo:
            return True, self.location_id
        if self.location_dest_id and self.location_dest_id.bloquea_grupo:
            return True, self.location_dest_id
        
        return False, None

    @api.model
    def create(self, vals):
        if self.env.user.has_group('biocell_bloqueo_ubicaciones.group_restriction_cambios_lote'):
            location_id = vals.get('location_id', False)
            location_dest_id = vals.get('location_dest_id', False)
            
            if location_id:
                location = self.env['stock.location'].browse(location_id)
                if location.bloquea_grupo:
                    raise UserError(_(
                        'No tiene permisos para crear pickings con la ubicación de origen "%s". '
                        'Esta ubicación está bloqueada para su grupo.'
                    ) % location.complete_name)
            
            if location_dest_id:
                location_dest = self.env['stock.location'].browse(location_dest_id)
                if location_dest.bloquea_grupo:
                    raise UserError(_(
                        'No tiene permisos para crear pickings con la ubicación de destino "%s". '
                        'Esta ubicación está bloqueada para su grupo.'
                    ) % location_dest.complete_name)
        
        return super(StockPicking, self).create(vals)

    def unlink(self):
        for picking in self:
            is_restricted, location = picking._check_restricted_location()
            if is_restricted:
                raise UserError(_(
                    'No tiene permisos para eliminar pickings con la ubicación "%s". '
                    'Esta ubicación está bloqueada para su grupo.'
                ) % location.complete_name)
        return super(StockPicking, self).unlink()

    def write(self, vals):
        if self.env.user.has_group('biocell_bloqueo_ubicaciones.group_restriction_cambios_lote'):
            for picking in self:
                location_id = vals.get('location_id', False)
                location_dest_id = vals.get('location_dest_id', False)
                
                if not location_id and picking.location_id:
                    location_id = picking.location_id.id
                if not location_dest_id and picking.location_dest_id:
                    location_dest_id = picking.location_dest_id.id
                
                is_restricted, location = picking._check_restricted_location(
                    location_id=location_id,
                    location_dest_id=location_dest_id
                )
                if is_restricted:
                    raise UserError(_(
                        'No tiene permisos para editar pickings con la ubicación "%s". '
                        'Esta ubicación está bloqueada para su grupo.'
                    ) % location.complete_name)
        
        return super(StockPicking, self).write(vals)

