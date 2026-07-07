from odoo import models, fields, api, _

class AccountAnalyticJournal(models.Model):
    _inherit='account.analytic.journal'
    
    serie_invoice = fields.Many2one(
        'it.invoice.serie', 
        string='Serie de Factura'
    )
    serie_sale_slip = fields.Many2one(
        'it.invoice.serie', 
        string='Serie de Boleta de Venta'
    )
    serie_credit_note= fields.Many2many(
        'it.invoice.serie', 
        string='Serie de Nota de Credito'
    )
