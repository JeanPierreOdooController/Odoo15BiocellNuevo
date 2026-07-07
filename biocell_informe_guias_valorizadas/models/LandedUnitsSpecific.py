from odoo import models, fields,api
from odoo.exceptions import UserError
import base64


class LandedUnitsSpecific(models.Model):
    _inherit="landed.units.specific"
    
    
    def generate_excel(self):
        import io
        from xlsxwriter.workbook import Workbook
        from xlsxwriter.utility import xl_rowcol_to_cell

        ReportBase = self.env['report.base']
        direccion = self.env['account.main.parameter'].search([('company_id','=',self.company_id.id)],limit=1).dir_create_file

        if not direccion:
            raise UserError(u'No existe un Directorio Exportadores configurado en Parametros Principales de Contabilidad para su Compañía')

        workbook = Workbook(direccion +'Reporte_GV.xlsx')
        workbook, formats = ReportBase.get_formats(workbook)

        numbertotalocho = workbook.add_format({'num_format':'0.00000000','bold': True})
        numbertotalocho.set_align('right')
        numbertotalocho.set_align('vcenter')
        numbertotalocho.set_border(style=1)
        numbertotalocho.set_font_size(10.5)
        numbertotalocho.set_font_name('Times New Roman')
        numbertotalocho.set_underline()

        import importlib
        import sys
        importlib.reload(sys)

        worksheet = workbook.add_worksheet("GV")
        worksheet.set_tab_color('blue')

        HEADERS = ['REFERENCIA','DE','PARA','PRODUCTO','UNIDAD','CANTIDAD','P.UNIT','VALOR','FACTOR','GASTO V','ADVALOREM','VALOR TOTAL','C.UNIT','PROVEEDOR','FCH. KARDEX']
        worksheet = ReportBase.get_headers(worksheet,HEADERS,0,0,formats['boldbord'])

        x=1
        init = 1

        for line in self.detalle_ids:
            stockmove = self.env["stock.move"].sudo().search(
                [
                    ("picking_id","=",line.picking_rel.id),
                    ("product_id","=",line.producto_rel.id)
                ],limit=1
            )
            
            worksheet.write(x,0,line.picking_rel.display_name if line.picking_rel else '',formats['especial1'])
            worksheet.write(x,1,line.origen_rel.display_name if line.origen_rel else '',formats['especial1'])
            worksheet.write(x,2,line.destino_rel.display_name if line.destino_rel else '',formats['especial1'])
            worksheet.write(x,3,line.producto_rel.display_name if line.producto_rel else '',formats['especial1'])
            worksheet.write(x,4,line.unidad_rel.display_name if line.unidad_rel else '',formats['especial1'])
            worksheet.write(x,5,line.cantidad_rel if line.cantidad_rel else 0,formats['numberdos'])
            worksheet.write(x,6,line.precio_unit_signed if line.precio_unit_signed else 0,formats['numberocho'])
            worksheet.write(x,7,line.valor_rel_signed if line.valor_rel_signed else 0,formats['numberdos'])
            worksheet.write(x,8,line.factor if line.factor else '',formats['numberocho'])
            worksheet.write(x,9,line.flete if line.flete else '',formats['numberocho'])
            worksheet.write(x,10,line.advalorem if line.advalorem else '',formats['numberdos'])
            worksheet.write(x,11,line.total if line.total else '',formats['numberdos'])
            worksheet.write(x,12,line.total/line.cantidad_rel if line.cantidad_rel and line.cantidad_rel != 0 else 0,formats['numberocho'])
            worksheet.write(x,13,line.picking_rel.partner_id.display_name if line.picking_rel.partner_id else '',formats['especial1'])
            worksheet.write(x,14,stockmove.kardex_date if stockmove.kardex_date else '',formats['reverse_dateformat'])
            x += 1

        # .strftime('%d/%m/%Y')
        worksheet.write_formula(x,5, '=SUM(' + xl_rowcol_to_cell(init,5) + ':' + xl_rowcol_to_cell(x-1,5) + ')', formats['numbertotal'])
        worksheet.write_formula(x,7, '=SUM(' + xl_rowcol_to_cell(init,7) + ':' + xl_rowcol_to_cell(x-1,7) + ')', formats['numbertotal'])
        worksheet.write_formula(x,9, '=SUM(' + xl_rowcol_to_cell(init,9) + ':' + xl_rowcol_to_cell(x-1,9) + ')', numbertotalocho)
        worksheet.write_formula(x,10, '=SUM(' + xl_rowcol_to_cell(init,10) + ':' + xl_rowcol_to_cell(x-1,10) + ')', formats['numbertotal'])
        worksheet.write_formula(x,11, '=SUM(' + xl_rowcol_to_cell(init,11) + ':' + xl_rowcol_to_cell(x-1,11) + ')', formats['numbertotal'])

        widths = [15,25,20,30,15,15,20,20,20,20,20,20,17,20,20]
        worksheet = ReportBase.resize_cells(worksheet,widths)
        workbook.close()

        f = open(direccion +'Reporte_GV.xlsx', 'rb')

        return self.env['popup.it'].get_file('Reporte GV.xlsx',base64.encodestring(b''.join(f.readlines())))
