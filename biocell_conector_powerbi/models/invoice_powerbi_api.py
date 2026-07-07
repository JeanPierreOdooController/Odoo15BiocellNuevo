from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class InvoicePowerApi(models.Model):
    _name = 'invoice.powerbi.api'
    _description = 'API PowerBI Ventas'
    _auto=False

    product_code = fields.Char('Código de Producto')
    product_description = fields.Char('Descripcion del Producto')
    client = fields.Char('Cliente')
    patient_name = fields.Char('Paciente')
    doctor_name = fields.Char('Medico')
    invoice_number = fields.Char('Numero de la factura')
    sale_order = fields.Char('SO')
    invoice_date = fields.Char('Fecha Facturacion')
    invoice_expiration_date = fields.Char('Fecha Venc. Factura')
    commercial_advisor = fields.Char('Asesor Comercial')
    sale_qty = fields.Float('Cantidad Vendida')

    real_currency = fields.Char('Moneda Fact. Real')
    real_price = fields.Float('Precio Fact. Real')

    currency = fields.Char('Moneda Fact. Convertida')
    price = fields.Float('Precio Fact. Convertida')

    total_income = fields.Float('Total Ingreso')
    igv_amount = fields.Float('IGV')
    total_income_with_igv= fields.Float('Total Ingreso + IGV')
    document_type = fields.Char('Tipo de Documento')
    

    def get_report(self):
        self.env.cr.execute(f"""
        CREATE OR REPLACE view invoice_biocell_conector_powerbi AS (
            SELECT 
                row_number() OVER () AS id, 
                T.*
            FROM(
                {''.join(self.get_sql())}
            ) AS T
        )
        """)
        return {
            'name': 'PowerBi Facturas',
            'type': 'ir.actions.act_window',
            'res_model': 'invoice.powerbi.api',
            'view_mode': 'tree',
            'view_type': 'form',
        }

    def get_sql(self,filters:list=[]):
        return [
            self.get_with(),
            self.get_select(),
            self.get_from(),
            self.get_where(filters)
        ]

    def get_with(self):
        return f"""
        WITH
            pen_invoices AS (
                SELECT
                    move_line.id AS move_line_id,

                    CASE
                        WHEN move.move_type = 'out_refund' THEN -1
                        ELSE 1
                    END *
                    CASE
                        WHEN currency.name <> 'PEN' THEN (move.currency_rate * move_line.price_unit)
                        ELSE move_line.price_unit
                    END AS price,

                    CASE
                        WHEN move.move_type = 'out_refund' THEN -1
                        ELSE 1
                    END *
                    CASE
                        WHEN currency.name <> 'PEN' THEN (move.currency_rate * move_line.l10n_pe_dte_price_unit_excluded)
                        ELSE move_line.l10n_pe_dte_price_unit_excluded
                    END AS total_income,

                    CASE
                        WHEN move.move_type = 'out_refund' THEN -1
                        ELSE 1
                    END *
                    CASE
                        WHEN currency.name <> 'PEN' THEN 
                            (move.currency_rate * move_line.l10n_pe_dte_price_unit_included) 
                        - (move.currency_rate * move_line.l10n_pe_dte_price_unit_excluded)
                        ELSE 
                            move_line.l10n_pe_dte_price_unit_included - move_line.l10n_pe_dte_price_unit_excluded
                    END AS igv_amount,

                    CASE
                        WHEN move.move_type = 'out_refund' THEN -1
                        ELSE 1
                    END *
                    CASE
                        WHEN currency.name <> 'PEN' THEN (move.currency_rate * move_line.price_total)
                        ELSE move_line.price_total
                    END AS total_income_with_igv

                FROM account_move_line AS move_line
                    LEFT JOIN account_move AS move ON move.id = move_line.move_id
                    LEFT JOIN res_currency AS currency ON currency.id = move.currency_id
                WHERE
                    move.company_id IS NOT NULL
                    AND move_line.display_type IS NULL
                    AND move_line.product_id IS NOT NULL
                    AND move_line.name NOT LIKE 'IGV-VEN'
                    AND move.move_type IN ('out_invoice', 'out_refund')
                    AND move.state = 'posted'
                    AND move_line.price_unit >= 0
            )
        """
    def get_select(self):
        return """
        SELECT
            product.default_code AS product_code,
            product_template.name AS product_description,
            client.name AS client,
            sale.name_patient AS patient_name,
            doctor.name AS doctor_name,
            move.ref AS invoice_number,
            sale.name AS sale_order,
            TO_CHAR (move.invoice_date - interval '5 hours' , 'DD/MM/YYYY') AS invoice_date,
            TO_CHAR (move.invoice_date_due - interval '5 hours', 'DD/MM/YYYY') AS invoice_expiration_date,
            invoice_partner.name AS commercial_advisor,
            move_line.quantity AS sale_qty,
            currency.name AS real_currency,

            CASE
                WHEN move.move_type = 'out_refund' THEN move_line.price_unit * -1
                ELSE move_line.price_unit
            END AS real_price,

            'PEN' AS currency,

            CASE
                WHEN move.move_type = 'out_refund' THEN pen_invoice.price * -1
                ELSE pen_invoice.price
            END AS price,

            CASE
                WHEN move.move_type = 'out_refund' THEN pen_invoice.total_income * -1
                ELSE pen_invoice.total_income
            END AS total_income,

            CASE
                WHEN move.move_type = 'out_refund' THEN  pen_invoice.igv_amount * -1
                ELSE pen_invoice.igv_amount
            END AS igv_amount,

            CASE
                WHEN move.move_type = 'out_refund' THEN pen_invoice.total_income_with_igv * -1
                ELSE pen_invoice.total_income_with_igv
            END AS total_income_with_igv,
            document_type.name AS document_type
        """

    def get_from(self):
        return """
        FROM account_move_line AS move_line
            LEFT JOIN account_move AS move ON move.id = move_line.move_id
            LEFT JOIN res_currency AS currency ON currency.id = move_line.currency_id
            LEFT JOIN product_product AS product ON product.id = move_line.product_id
            LEFT JOIN product_template AS product_template ON product_template.id = product.product_tmpl_id
            LEFT JOIN res_partner AS client ON client.id = move.partner_id
            LEFT JOIN res_users AS invoice_user ON invoice_user.id = move.invoice_user_id
            LEFT JOIN res_partner AS invoice_partner ON invoice_partner.id = invoice_user.partner_id
            LEFT JOIN l10n_latam_document_type AS document_type ON document_type.id = move.l10n_latam_document_type_id
            LEFT JOIN sale_order AS sale ON sale.name = move.invoice_origin
            LEFT JOIN res_partner AS doctor ON doctor.id = sale.name_doctor
            LEFT JOIN pen_invoices AS pen_invoice ON pen_invoice.move_line_id = move_line.id
        """

    def get_where(self,filters:list=[]):
        where_sql="""
        WHERE
            move.company_id IS NOT NULL
            AND move_line.display_type IS NULL
            AND move_line.product_id IS NOT NULL
            AND move_line.name NOT LIKE 'IGV-VEN'
            AND move.move_type IN ('out_invoice', 'out_refund')
            AND move.state = 'posted'
            AND move_line.price_unit >= 0
        """
        if filters:
            where_sql+=filters
        return where_sql
    
    def get_order_by(self):
        return """
        """
