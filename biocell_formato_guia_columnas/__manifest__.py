#-*- enconding:utf-8 -*- 
{
    'name': 'Reporte Guias por lote',
    'version': '1.0',
    'description': 'Modulo que modifica el reporte de "Guias" para que el contenido este separado por lotes',
    'author': 'ITGRUPO, Jhorel Revilla Calderon',
    'license': 'LGPL-3',
    'depends': [
        'biocell_pe_facturacion_electronica'
    ],
    'data': [
        'views/report_inherit.xml'
    ],
    'auto_install': False,
    'application': False
}
