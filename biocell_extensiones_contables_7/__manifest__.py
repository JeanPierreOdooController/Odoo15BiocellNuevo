# -*- coding: utf-8 -*-
{
    'name': "Campos en movimientos de producto",
    'author': 'ITGRUPO, Alessandro Pelayo Mollocondo Medrano',
    'category': 'Kadex',
    'description': """Modulo enfocado para poder mostrar campos nativos de odoo, en los stock.move y stock.move.line, en este caso se estan habilitando la visualizacion """,
    'version': '1.0',
    'summary': 'Modificaciones personalizadas para kardex',
    'depends': ['stock', 'biocell_kardex_movimientos_fisicos'],
    'data': [
        'views/views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}