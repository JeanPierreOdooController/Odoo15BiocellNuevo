# -*- coding: utf-8 -*-
{
    'name': "Order Line Original",
    'author': 'ITGRUPO, Alessandro Pelayo Mollocondo Medrano',
    'category': 'sale',
    'description': """Crear tabla con las lineas de pedido ya ejecutadas y que se copien hasta antes de la confirmación""",
    'version': '1.0',
    'summary': 'Modificaciones personalizadas para sale',
    'depends': ['sale', 'payment', 'uom', 'utm', 'stock', 'biocell_meta_comercial'],
    'data': [
        'security/ir.model.access.csv',
        'views/agregar.xml',
        'views/agrear_order.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}