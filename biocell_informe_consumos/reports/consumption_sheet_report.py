from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ConsumptionSheetReport(models.Model):
    _name = 'consumption.sheet.report'
    _description = 'Reporte de Hoja de Consumo'
    _auto = False

    sale_order_id = fields.Many2one("sale.order", string="Pedido de Venta")
    patient_name = fields.Char(string="Nombre paciente")
    medical_center_id = fields.Many2one("res.partner", string="Centro medico")
    surgeon_id = fields.Many2one("res.partner", string="Cirujano")
    state = fields.Selection([
        ('draft','Borrado'),
        ('waiting','Esperando otra operación'),
        ('confirmed','Esperando'),
        ('assigned','Listo'),
        ('done','Realizado'),
        ('cancel','Cancelado'),
    ], string="Estado")
    product_code = fields.Char(string="Código de Producto")
    product_description = fields.Char(string="Descripción de Producto")
    surgery_date = fields.Datetime(string="Fecha/Hora Cirugía")

    product_qty_consumed = fields.Float(string="Cantidad Consumida")
    product_unit_price = fields.Float(string="Precio Unitario")
    product_total_price = fields.Float(string="Precio Total")
    subtotal = fields.Float(string="Subtotal")
    tax_amount = fields.Float(string="igv")
    total_amount = fields.Float(string="Total")
    total_consumed_amount = fields.Float(string="Total Consumido")

    """"""

    def get_report(self):
        self.env.cr.execute(f"""
            CREATE OR REPLACE view consumption_sheet_report as (
                SELECT row_number() OVER () AS id, T.* FROM({self.get_sql()} ) AS T
            )
        """)
        return {
            'name': 'Reporte de Hoja de Consumo',
            'type': 'ir.actions.act_window',
            'res_model': 'consumption.sheet.report',
            'view_mode': 'tree',
            'view_type': 'form',
        }

    def get_sql(self):
        return ' '.join([
            self.get_sql_WITH(),
            self.get_sql_SELECT(),
            self.get_sql_FROM(),
            self.get_sql_WHERE(),
        ])

    def get_sql_WITH(self):
        return """
        WITH total_consummed AS (
            SELECT
                sale_line.order_id as sale_id,
                SUM(move_line.qty_consumida) as total_consummed,
                SUM(
                    COALESCE(move_line.qty_consumida, 0) * 
                    (COALESCE(sale_line.price_subtotal,0) / NULLIF(sale_line.product_uom_qty,0))
                ) AS subtotal
            FROM stock_move_line AS move_line
                LEFT JOIN stock_move AS move ON move.id = move_line.move_id
                LEFT JOIN sale_order_line AS sale_line ON sale_line.id = move.sale_line_id
            GROUP BY
                sale_line.order_id
        ),
        sale_invoices AS (
            SELECT
                sale_line.order_id AS order_id,
                STRING_AGG(sale_invoice_rel.invoice_line_id :: TEXT, ',') AS invoices
            FROM sale_order_line_invoice_rel AS sale_invoice_rel
                LEFT JOIN sale_order_line AS sale_line ON sale_line.id = sale_invoice_rel.order_line_id
            GROUP BY
                sale_line.order_id
        )
        """

    def get_sql_SELECT(self):
        return """
        SELECT
            sale.id AS sale_order_id,
            sale.name_patient AS patient_name,
            sale.medic_center AS medical_center_id,
            sale.name_doctor AS surgeon_id,
            picking.state AS state,
            template.default_code AS product_code,
            template.name AS product_description,
            sale.sugery_date AS surgery_date,
            move_line.qty_consumida AS product_qty_consumed,
            (COALESCE(sale_line.price_subtotal,0) / NULLIF(sale_line.product_uom_qty,0)) AS product_unit_price,
            (
                COALESCE(move_line.qty_consumida, 0) * 
                (COALESCE(sale_line.price_subtotal,0) / NULLIF(sale_line.product_uom_qty,0))
            )::NUMERIC AS product_total_price,
            total_consummed.subtotal:: NUMERIC AS subtotal,
            COALESCE(total_consummed.subtotal, 0) * 0.18 AS tax_amount,
            total_consummed.subtotal + (COALESCE(total_consummed.subtotal, 0) * 0.18) AS total_amount,
            total_consummed.total_consummed AS total_consumed_amount
        """
    
    def get_sql_FROM(self):
        return """
        FROM 
            stock_move_line AS move_line
            LEFT JOIN stock_move AS move ON move.id  =  move_line.move_id 
            LEFT JOIN stock_picking AS picking ON picking.id = move.picking_id
            LEFT JOIN sale_order AS sale ON sale.id = move.sale_id_return
            LEFT JOIN sale_order_line AS sale_line ON sale_line.id = move.sale_line_id
            LEFT JOIN product_product AS product ON product.id = move.product_id
            LEFT JOIN product_template AS template ON template.id = product.product_tmpl_id
            LEFT JOIN total_consummed AS total_consummed ON total_consummed.sale_id = sale.id
            LEFT JOIN sale_invoices AS sale_invoices ON sale_invoices.order_id = sale.id
        """
    
    def get_sql_WHERE(self):
        return """
        WHERE
            move.sale_id_return IS NOT NULL
            AND sale_invoices.invoices IS NULL
            AND move_line.qty_consumida > 0
        """
