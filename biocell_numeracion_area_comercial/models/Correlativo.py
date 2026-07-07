from odoo import fields, models, api, _
import time
from datetime import datetime

class Correlativo(models.Model):
    _inherit="sale.order"
    
    @api.model
    def create(self, vals):

        today_month = str(datetime.today().month)
        today_year  = str(datetime.today().year)

        first = 'SO'
        second = (today_year + '-')

        if len(str(datetime.today().month)) == 1:
            second += '0' + today_month
        elif len(str(today_month)) == 2:
            second += today_month


        id_seq = self.env['ir.sequence'].sudo().search([('name','=','Correlativo Biocell Sale-'+second)], limit=1)

        if not id_seq:
            id_seq = self.env['ir.sequence'].sudo().create({
                'name': 'Correlativo Biocell Sale-'+second,
                'implementation': 'no_gap',
                'active': True,
                'prefix': '',
                'padding': 5,
                'number_increment': 1,
                'number_next_actual': 1
            })

        

        res = super(Correlativo,self).create(vals)

        third = res.shop_id.codigo
        sequence = id_seq._next()
        name = first + '-' + second + '-' + third + '-' + sequence

        res.name = name
        return res