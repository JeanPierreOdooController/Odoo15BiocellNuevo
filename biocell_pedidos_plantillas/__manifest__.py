# -*- coding: utf-8 -*-
{
    'name': "Plantilla de Cotización Edit",
    'author': 'ITGRUPO, Alessandro Pelayo Mollocondo Medrano',
    'category': 'Purchases',
    'description': """Agregar campos para poder ser utilizado en filtros adecuados""",
    'version': '1.0',
    'summary': 'Modificaciones personalizadas para sale',
    'depends': ['sale_management'],
    'data': [
        'security/grupo.xml',
        'security/ir.model.access.csv',
        'views/sale_category.xml',
        'views/sale_type_category.xml',
        'views/agregar.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}