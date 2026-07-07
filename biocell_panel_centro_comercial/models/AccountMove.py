from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleAdvancePaymentInv(models.Model):
    _inherit = "account.move"
    
    shop_id=fields.Many2one(
        'account.analytic.journal',
        string="Centro"
    )
    
    serie_domain=fields.Many2many(
        'it.invoice.serie',
        compute="_compute_serie_domain"
    )
    
    
    @api.depends('shop_id','l10n_latam_document_type_id')
    def _compute_serie_domain(self):
        for r in self:
            domain=[]
            if not r.shop_id or not r.l10n_latam_document_type_id:
                domain=self.env['it.invoice.serie'].search([]).ids
            # Facturas
            elif r.l10n_latam_document_type_id.code=='01':
                domain.append(r.shop_id.serie_invoice.id)
            # Boleta de Venta
            elif r.l10n_latam_document_type_id.code=='03':
                domain.append(r.shop_id.serie_sale_slip.id)
            # Nota de Credito
            elif r.l10n_latam_document_type_id.code=='07':
                domain.extend(r.shop_id.serie_credit_note.ids)
            else:
                domain=False
            r.serie_domain=domain
        