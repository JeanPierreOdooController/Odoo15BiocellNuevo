from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class InventoryPowerApi(models.Model):
    _name = 'inventory.powerbi.api'
    _description = 'API PowerBI Inventario'
    _auto=False

    product_code = fields.Char('Código de Item')
    product_description = fields.Char('Descripción del Item')
    unit_cost = fields.Float('Costo Unitario')
    total_cost = fields.Float('Costo Total')
    warehouse = fields.Char('Nombre Almacen')
    available_qty = fields.Float('Cantidad Disponible')
    total_qty = fields.Float('Cantidad Total')
    lot = fields.Char('Lote')
    create_date = fields.Char('Fecha de Creación')
    expiration_date = fields.Char('Fecha de Vencimiento')
    group = fields.Char('Grupo')
    subgroup = fields.Char('Subgrupo')
    
    def get_report(self):
        # kardex by lot
        self.env['stock.balance.report.lote'].get_balance_view()
        # kardex valued
        self.env['temporal.valued.kardex'].get_report()

        self.env.cr.execute(f"""
        CREATE OR REPLACE view inventory_biocell_conector_powerbi as (
            SELECT 
                row_number() OVER () AS id, 
                T.*
            FROM(
                {''.join(self.get_sql())}
            ) AS T
        )
        """)
        return {
            'name': 'PowerBi Inventario',
            'type': 'ir.actions.act_window',
            'res_model': 'inventory.powerbi.api',
            'view_mode': 'tree',
            'view_type': 'form',
        }

    def get_sql(self):
        return [
            self.get_with(),
            self.get_select(),
            self.get_from(),
            self.get_where(),
        ]

    def get_with(self):
        return f"""
        WITH kardex_valued_cost AS (
            SELECT *
            FROM (
                SELECT
                    temporal_kardex.date,
                    temporal_kardex.product_id,
                    temporal_kardex.location_id,
                    temporal_kardex.lot_id,
                    temporal_kardex.unit_cost,
                    temporal_kardex.total_cost,
                    ROW_NUMBER() OVER (
                        PARTITION BY temporal_kardex.product_id, temporal_kardex.location_id, temporal_kardex.lot_id
                        ORDER BY temporal_kardex.date DESC
                    ) AS row_num
                FROM temporal_valued_kardex AS temporal_kardex
                WHERE temporal_kardex.unit_cost > 0
            ) AS ranked
            WHERE ranked.row_num = 1
        )
        """
    def get_select(self):
        return """
        SELECT
            kardex_by_lot.codigo AS product_code,             
            product_tmpl.name AS product_description,
            kardex_valued.unit_cost AS unit_cost,
            kardex_valued.unit_cost * kardex_by_lot.entrada AS total_cost,
            location.complete_name AS warehouse,
            kardex_by_lot.saldo AS available_qty,
            kardex_by_lot.entrada AS total_qty,
            lot.name AS lot,
            TO_CHAR(lot.create_date,'DD/MM/YYYY') AS create_date,
            TO_CHAR(lot.expiration_date,'DD/MM/YYYY') AS expiration_date,
            kardex_by_lot.categoria_1 AS group,
            kardex_by_lot.categoria_2 AS subgroup
        """
    def get_from(self):
        return """
        FROM 
            biocell_panel_saldos_financieros_4_lote AS kardex_by_lot
            LEFT JOIN product_product AS product ON product.id = kardex_by_lot.producto
            LEFT JOIN product_template AS product_tmpl ON product_tmpl.id = product.product_tmpl_id
            LEFT JOIN stock_location AS location ON location.id = kardex_by_lot.almacen
            LEFT JOIN stock_production_lot AS lot ON lot.id = kardex_by_lot.lote
            LEFT JOIN kardex_valued_cost AS kardex_valued ON (
                kardex_valued.product_id = product.id AND
                kardex_valued.location_id = location.id AND
                kardex_valued.lot_id = lot.id
            )
        """
    def get_where(self):
        return f"""
        WHERE
            location.company_id = {self.env.company.id} 
        """