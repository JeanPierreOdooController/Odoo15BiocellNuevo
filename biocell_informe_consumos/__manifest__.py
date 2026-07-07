# -*- enconding:utf-8 -*-
{
    'name': 'Reporte de Hoja de Consumo',
    'version': '1.0',
    'description': 'Reporte de Hoja de Consumo',
    'author': 'ITGRUPO, Jhorel Revilla',
    'license': 'LGPL-3',
    'depends': [
        'biocell_devoluciones_comerciales_stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/consumption_sheet_report.xml'
    ],
    'auto_install': False,
    'application': False,
}