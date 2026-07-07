# Copyright 2017 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class PartnerXlsx(models.AbstractModel):
    _name = "report.biocell_generador_excel.partner_xlsx"
    _inherit = "report.biocell_generador_excel.abstract"
    _description = "Partner XLSX Report"

    def generate_xlsx_report(self, workbook, data, partners):
        ws = workbook.create_sheet("Report")
        for i, obj in enumerate(partners):
            ws.append([obj.name])
