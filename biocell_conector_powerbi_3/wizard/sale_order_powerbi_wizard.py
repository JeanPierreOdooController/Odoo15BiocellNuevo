from odoo import models, fields, api

class SaleOrderPowerbiWizard(models.TransientModel):
    _name="sale.order.powerbi.wizard"
    
    def get_report(self):
        self.env.cr.execute(f"""
            CREATE OR REPLACE view biocell_conector_powerbi_3 as ( {self._get_sql()} )
        """)
        return {
            'name': 'PowerBi Ventas',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.powerbi',
            'view_mode': 'tree',
            'view_type': 'form',
        }
    
    def _get_sql(self):
        sql = """
        SELECT row_number() OVER () AS id, T.* FROM(
            SELECT
                so.name AS sale_order,
                pt.default_code AS product_code,
                so.create_date - INTERVAL '5 hours' AS create_datetime,
                so.confirmation_date AS confirmation_datetime,
                CASE
                    WHEN solo.product_id IS NOT NULL 
                        THEN solo.product_uom_qty
                    ELSE
                        0
                END AS quotation_qty,
                stock_sent.qty AS sent_qty,
                stock_consumed.qty AS consumed_qty,
                client.name AS partner_id,
                asesor.name AS saleperson_id,
                created_by.name AS created_by_id,
                
                (
                    SELECT
                        string_agg(sot.name,' ; ')
                    FROM
                        sale_order_sale_order_template_rel as sot_rel
                        LEFT JOIN sale_order_template AS sot ON sot_rel.template_id = sot.id
                    WHERE
                        sot_rel.order_id = so.id AND
                        sot.sale_type = 'sale'
                ) AS plantilla_presupuesto_id,

                (
                    SELECT
                        string_agg(sot.name,' ; ')
                    FROM
                        sale_order_sale_order_template_rel_kardex as sot_rel
                        LEFT JOIN sale_order_template AS sot ON sot_rel.template_id = sot.id
                    WHERE
                        sot_rel.order_id = so.id AND
                        sot.sale_type = 'stock'
                ) AS plantilla_kardex_id,                
                medic_center.name AS medic_center,
                name_doctor.name AS name_doctor,
                so.sugery_date AS sugery_date,
                pc.name AS procedure_clinic_id,
                so.request_date AS request_date,
                so.schedulling_request_date AS schedulling_request_date,
                CASE 
                    WHEN sot.sale_type = 'sale' THEN sot.name
                    ELSE NULL
                END AS plantilla_presupuesto_line_id,
                
                CASE 
                    WHEN sot.sale_type = 'stock' THEN sot.name
                    ELSE NULL
                END AS plantilla_kardex_line_id
            FROM
                sale_order_line AS sol
                LEFT JOIN product_product AS pp ON sol.product_id = pp.id
                LEFT JOIN product_template AS pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN sale_order AS so ON sol.order_id = so.id
                LEFT JOIN biocell_pedidos_comerciales_2 AS solo ON solo.order_line_id = sol.id 
                LEFT JOIN(
                    SELECT
                        sum(sml.qty_done) AS qty,
                        sm.sale_line_id
                    FROM 
                        stock_move_line sml
                        INNER JOIN stock_move AS sm ON sm.id = sml.move_id
                        INNER JOIN stock_location AS sl ON sl.id = sm.location_id
                        LEFT JOIN stock_picking AS sp ON sp.id = sm.picking_id
                    WHERE
                        sp.location_dest_id = 39
                    GROUP BY 
                        sm.sale_line_id
                )stock_sent ON stock_sent.sale_line_id = sol.id
                LEFT JOIN(
                    SELECT
                        sum(sml.qty_done) AS qty,
                        sm.sale_line_id
                    FROM 
                        stock_move_line sml
                        INNER JOIN stock_move AS sm ON sm.id = sml.move_id
                        INNER JOIN stock_location AS sl ON sl.id = sm.location_id
                        LEFT JOIN stock_picking AS sp ON sp.id = sm.picking_id
                    WHERE
                        sp.location_dest_id = 5
                    GROUP BY 
                        sm.sale_line_id
                )stock_consumed ON stock_consumed.sale_line_id = sol.id
                LEFT JOIN sale_order_template AS sot ON sot.id = sol.sale_order_template_id
                LEFT JOIN res_partner AS client ON so.partner_id = client.id
                LEFT JOIN res_users AS asesor_user ON so.user_id = asesor_user.id
                LEFT JOIN res_partner AS asesor ON asesor_user.partner_id = asesor.id
                LEFT JOIN res_users AS created_by_user ON so.create_uid = created_by_user.id
                LEFT JOIN res_partner AS created_by ON created_by_user.partner_id = created_by.id
                LEFT JOIN res_partner AS medic_center ON so.medic_center = medic_center.id
                LEFT JOIN res_partner AS name_doctor ON so.name_doctor = name_doctor.id
                LEFT JOIN procedure_clinic AS pc ON so.procedure_clinic_id = pc.id
            WHERE
                sol.sale_type = 'sale' AND
                sol.product_id IS NOT NULL
        ) T
        """
        return sql