from odoo import models, fields, api
from odoo.exceptions import UserError
import base64, io, openpyxl


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    lotes_file_xlsx = fields.Binary('Nro de Lotes', help="Archivo xlsx (Cod Producto, Nro Lote, Cantidad)")
    errores_txt_xlsx = fields.Text("Errores de Importación Lotes")
    remove_rest_xlsx = fields.Boolean("Remover líneas que no están en el archivo a importar", default=True)

    def get_read_lotes_xlsx(self):
        for picking in self:

            if not picking.lotes_file_xlsx:
                raise UserError("Debe cargar un archivo de importación xlsx.")

            if not picking.location_id:
                raise UserError("El picking no tiene ubicación de origen.")

            # Leer Excel
            file_content = base64.b64decode(picking.lotes_file_xlsx)
            wb = openpyxl.load_workbook(io.BytesIO(file_content), data_only=True)
            ws = wb.active

            datos = []
            errores = []

            for index, row in enumerate(ws.iter_rows(min_row=1, values_only=True), start=1):
                # Ignorar filas totalmente vacías (basura de Excel)
                if not row or (not row[0] and not row[1] and row[2] is None):
                    continue

                # Si hay datos pero falta algo obligatorio → error
                if not row[0] or not row[1] or row[2] is None:
                    errores.append(f"Fila {index}: fila incompleta (producto, lote o cantidad).")
                    continue

                cod_producto = str(row[0]).strip()
                lote = str(row[1]).strip()

                # Validar cantidad
                try:
                    cantidad = float(row[2])
                except:
                    errores.append(f"Fila {index}: cantidad inválida para {cod_producto} / {lote}.")
                    continue

                # 1) Validar que el producto exista
                producto = self.env['product.product'].search([('default_code', '=', cod_producto)], limit=1)
                if not producto:
                    errores.append(f"Fila {index}: no existe el producto: {cod_producto}")
                    continue

                # 2) Validar que el lote pertenezca al producto
                lot_obj = self.env['stock.production.lot'].search([
                    ('name', '=', lote),
                    ('product_id', '=', producto.id)
                ], limit=1)

                if not lot_obj:
                    errores.append(f"Fila {index}: el lote {lote} no pertenece al producto {cod_producto}")
                    continue

                # 3) Validar la cantidad disponible en ubicación origen
                quants = self.env['stock.quant'].search([
                    ('product_id', '=', producto.id),
                    ('lot_id', '=', lot_obj.id),
                    ('location_id', '=', picking.location_id.id),
                ])

                disponible = sum(quants.mapped('quantity')) - sum(quants.mapped('reserved_quantity'))

                if cantidad > disponible:
                    errores.append(
                        f"Fila {index}: cantidad ({cantidad}) mayor al disponible ({disponible}) "
                        f"del lote {lote} del producto {producto.display_name} en {picking.location_id.display_name}"
                    )
                    continue

                datos.append({
                    'product_id': producto.id,
                    'cantidad': cantidad,
                })

            # Si hay errores, NO importar nada
            if errores:
                picking.errores_txt_xlsx = "\n".join(errores)
                return

            # Crear movimientos solo si no hubo errores
            move_lines_vals = []
            for d in datos:
                prod_id = d['product_id']
                qty = d['cantidad']

                if not picking.move_lines.filtered(lambda m: m.product_id.id == prod_id):
                    product = self.env['product.product'].browse(prod_id)
                    move_lines_vals.append((0, 0, {
                        'name': product.display_name,
                        'product_id': prod_id,
                        'product_uom_qty': qty,
                        'product_uom': product.uom_id.id,
                        'location_id': picking.location_id.id,
                        'location_dest_id': picking.location_dest_id.id,
                    }))

            if move_lines_vals:
                picking.write({'move_lines': move_lines_vals})

            picking.errores_txt_xlsx = ""
        return True
