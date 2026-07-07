from datetime import datetime, timedelta
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class TemporalValuedKardex(models.Model):
    _name = 'temporal.valued.kardex'
    _description = 'Kardex Valorado Temporal'

    product_id = fields.Many2one('product.product', string='Producto')
    location_id = fields.Many2one('stock.location', string='Ubicación')
    lot_id = fields.Many2one('stock.production.lot', string='Lote')
    unit_cost = fields.Float('Costo Unitario')
    total_cost = fields.Float('Costo Total')
    date = fields.Date('Fecha')
    
    def get_report(self):
        self.env.cr.execute("DELETE FROM temporal_valued_kardex")
        self.env.cr.execute("ALTER SEQUENCE public.temporal_valued_kardex_id_seq RESTART WITH 1")

        self.env.cr.execute(self.get_sql())
        raw_kardex_data =self.env.cr.dictfetchall()

        batch_size = 100
        avg_cost_data={}
        data_to_create = []
        for idx,row in enumerate(raw_kardex_data):
            avg_cost, total_cost =self.compute_average_cost(row,avg_cost_data)
            data_to_create.append({
                'product_id':row.get('product_id',False),
                'location_id':row.get('location_id',False),
                'lot_id':row.get('lot_id',False),
                'date': row.get('fechax',False),
                'unit_cost': avg_cost, 
                'total_cost': total_cost
            })
            if idx % batch_size == 0 or idx == len(raw_kardex_data) - 1:
                self.create(data_to_create)
                data_to_create = []

    def get_sql(self):
        return f"""
        SELECT
            *
        FROM(
            {self.get_valued_kardex_select()}
            {self.get_valued_kardex_from()}
            {self.get_valued_kardex_where()}
        ) Total
        UNION
        ALL
        -- Kardex Save Period
        {self.get_save_kardex_select()}
        {self.get_save_kardex_from()}
        {self.get_order_by_sql()}
        """

    def get_valued_kardex_select(self):
        return f"""
        SELECT
            valued_kardex.product_id,
            valued_kardex.location_id,
            valued_kardex.lot_id,
            valued_kardex.debit,
            valued_kardex.credit,
            valued_kardex.ingreso,
            valued_kardex.salida,
            origin_location.usage AS origen_usage,
            destination_location.usage AS destino_usage,
            valued_kardex.fecha - interval '5' hour as fechax
        """
    def get_valued_kardex_from(self):
        return f"""
        FROM vst_kardex_fisico_valorado AS valued_kardex
            LEFT JOIN stock_move move_id ON move_id.id = valued_kardex.stock_moveid
            LEFT JOIN stock_location AS origin_location ON origin_location.id = move_id.location_id
            LEFT JOIN stock_location AS destination_location ON destination_location.id = move_id.location_dest_id
        """
    def get_valued_kardex_where(self):
        return f"""
        WHERE
            (
                fecha_num(
                    (valued_kardex.fecha - interval '5' hour) :: DATE
                ) BETWEEN '20240501'
                AND '{datetime.now().strftime("%Y%m%d")}'
            )
            AND valued_kardex.company_id = """ +str(self.env.company.id)+ """
        """
    def get_save_kardex_select(self):
        return f"""
        SELECT
            save_period.producto AS product_id,
            save_period.almacen AS location_id,
            lot.id AS lot_id,
            save_period.cprom * save_period.stock AS debit,
            0 AS credit,
            save_period.stock AS ingreso,
            0 AS salida,
            '' AS origen_usage,
            location_id.usage AS destino_usage,
            (fecha || ' 00:00:00')::timestamp as fechax
        """
    def get_save_kardex_from(self):
        return f"""
        FROM kardex_save_period AS save_period
            LEFT JOIN stock_production_lot AS lot ON lot.id = save_period.lote
            INNER JOIN stock_location AS location_id ON location_id.id = save_period.almacen
            JOIN (
                SELECT
                    kardex_save.id
                FROM kardex_save AS kardex_save
                    LEFT JOIN account_period_kardex AS kardex_period ON kardex_period.id = kardex_save.name
                WHERE
                    kardex_save.state = 'done'
                    AND kardex_save.company_id = """ +str(self.env.company.id)+ """
                ORDER BY
                    date_end DESC
                LIMIT
                    1
            ) AS last_save ON last_save.id = save_period.save_id
        """
    def get_order_by_sql(self):
        return f"""
        ORDER BY 
            location_id,
            product_id,
            fechax
        """
    def compute_average_cost(self,line, avg_cost_data):
        key = (line['product_id'], line['location_id'], line['lot_id'])
        accumulated = avg_cost_data.get(key, [0, 0])
        previous_avg_cost = accumulated[1] / accumulated[0] if accumulated[0] != 0 else 0


        origin_usage = line.get('origin_usage') or ''
        destination_usage = line.get('destination_usage') or ''

        quantity_in = line.get('ingreso') or 0
        quantity_out = line.get('salida') or 0
        debit = line.get('debit') or 0
        credit = line.get('credit') or 0

        if quantity_in or debit:
            accumulated[0] += quantity_in - quantity_out
            accumulated[1] += debit - credit
        else:
            if origin_usage == 'internal' and destination_usage == 'supplier':
                accumulated[0] -= quantity_out
                accumulated[1] -= debit + (credit * quantity_out)
            elif quantity_out:
                accumulated[0] += quantity_in - quantity_out
                accumulated[1] -= quantity_out * previous_avg_cost
                
            else:
                accumulated[0] += quantity_in - quantity_out
                accumulated[1] -= credit

        if accumulated[0] <= 0:
            accumulated[1] = 0

        current_avg_cost = accumulated[1] / accumulated[0] if accumulated[0] != 0 else 0
        avg_cost_data[key] = accumulated

        return current_avg_cost, accumulated[1]
