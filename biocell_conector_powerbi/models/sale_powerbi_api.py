from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class SalePowerApi(models.Model):
    _name = 'sale.powerbi.api'
    _description = 'API PowerBI Ventas-CRM'
    _auto=False

    sale_no = fields.Char('Número SO')
    establishment = fields.Char('Centro')
    quoted_amount = fields.Float('Monto cotizado')
    client_name = fields.Char('Cliente')
    doctor_name = fields.Char('Médico')
    medical_center_name = fields.Char('Centro Médico')
    surgery_date = fields.Char('Fecha y hora de cirugía')
    clinical_procedure = fields.Char('Procedimiento clínico')
    state = fields.Char('Etapa de venta')
    invoice_ref = fields.Char('Factura')
    invoice_amount = fields.Char('Monto factura')
    observations = fields.Char('Observaciones')
    saleman_assigned = fields.Char('Asignado a')
    
    def get_report(self):
        
        self.env.cr.execute(f"""
        CREATE OR REPLACE view sale_biocell_conector_powerbi as (
            SELECT 
                row_number() OVER () AS id, 
                T.*
            FROM(
                {''.join(self.get_sql())}
            ) AS T
        )
        """)
        return {
            'name': 'PowerBi CRM',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.powerbi.api',
            'view_mode': 'tree',
            'view_type': 'form',
        }

    def get_sql(self):
        return [
            self.get_with(),
            self.get_select(),
            self.get_from(),
            self.get_where(),
            self.get_order_by()
        ]

    def get_with(self):
        return f"""
        WITH last_sale_invoice AS (
            SELECT
                DISTINCT ON (sale_line.order_id)
                sale_line.order_id AS sale_id,
                invoice.ref AS invoice_ref,
                CONCAT(currency.symbol, invoice.amount_total) AS invoice_amount,
                saleman_partner.name AS saleman_name
            FROM sale_order_line AS sale_line
                LEFT  JOIN sale_order_line_invoice_rel AS sale_invoice_rel ON sale_invoice_rel.order_line_id  = sale_line.id
                LEFT JOIN account_move_line AS invoice_line ON invoice_line.id = sale_invoice_rel.invoice_line_id
                LEFT JOIN account_move AS invoice ON invoice.id = invoice_line.move_id
                LEFT JOIN res_currency AS currency ON currency.id = invoice.currency_id
                LEFT JOIN res_users AS saleman ON saleman.id = invoice.invoice_user_id 
                LEFT JOIN res_partner AS saleman_partner ON saleman_partner.id = saleman.partner_id
            WHERE
                invoice.move_type = 'out_invoice'
            ORDER BY
                sale_line.order_id,
                invoice.create_date DESC
        )
        """
    def get_select(self):
        return """
        SELECT
            sale.id AS sale_id,
            sale.name AS sale_no,
            establishment.name AS establishment,
            sale.amount_total AS quoted_amount,
            partner.vat as client_name,
            medic.vat AS doctor_name,
            medical_center.vat AS medical_center_name,
            sale.sugery_date AS surgery_date,
            clinical_procedure.name AS clinical_procedure,
            sale.state AS state,
            last_sale_invoice.invoice_ref AS invoice_ref,
            last_sale_invoice.invoice_amount AS invoice_amount,
            sale.note AS observations,
            last_sale_invoice.saleman_name AS saleman_assigned
        """

    def get_from(self):
        return """
        FROM sale_order AS sale
            LEFT JOIN account_analytic_journal AS establishment ON establishment.id = sale.shop_id        
            LEFT JOIN res_partner AS partner ON partner.id = sale.partner_id
            LEFT JOIN res_partner AS medic ON medic.id = sale.name_doctor
            LEFT JOIN res_partner AS medical_center ON medical_center.id = sale.medic_center
            LEFT JOIN procedure_clinic AS clinical_procedure ON clinical_procedure.id = sale.procedure_clinic_id
            LEFT JOIN last_sale_invoice AS last_sale_invoice ON last_sale_invoice.sale_id = sale.id
        """

    def get_where(self,filters:list=[]):
        if not filters:
            return ""
        return """
        WHERE
            
        """
    
    def get_order_by(self):
        return """
        ORDER BY
            sale.create_date DESC
        """
