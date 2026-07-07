# -*- encoding:utf-8 -*-
{
    'name': 'Campos opcionales-ALBARANES',
    'version': '1.0',
    'description': 'Modulo que coloca como campos opciones a:"Factura" y "Guia" en stock.picking',
    'author': 'ITGRUPO, Jhorel Revilla Calderon',
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'biocell_logistica_operativa',
        'biocell_kardex_movimientos_fisicos'
    ],
    'data': [
        'views/inherit_stock.xml'
    ],
    'auto_install': False,
    'application': False,
    'sequence': -1000
}