from odoo import models
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for picking in self:
            blocked_lines = []

            for move_line in picking.move_line_ids:
                product = move_line.product_id
                lot = move_line.lot_id

                # Solo si producto y lote están bloqueados
                if product.product_tmpl_id.block_transfers and lot and lot.block_transfers:
                    blocked_lines.append(
                        f"- {product.default_code} (Código de producto) - {lot.name} (Lote)"
                    )

            # Si hay líneas bloqueadas, mostrar un solo mensaje con lista completa
            if blocked_lines:
                blocked_text = "\n".join(blocked_lines)

                raise UserError(
                    f"No se puede validar el albarán {picking.name} porque cuenta con el/los siguiente(s) productos bloqueados:\n\n"
                    f"{blocked_text}\n\n"
                    f"Libere el/los producto(s) antes de validar."
                )

        return super().button_validate()
