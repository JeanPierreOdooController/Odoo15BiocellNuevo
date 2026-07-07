# -*- coding: utf-8 -*-
{
    'name': "Readonly lot production",
    'author': 'ITGRUPO, Alessandro Pelayo Mollocondo Medrano',
    'category': 'Lot',
    'description': """Modulo que permite que solo los usuarios que esten dentro del grupo puedo editar, y si se enceuntran fuera del grupo que este en solo leectura los campos designados""",
    'version': '1.0',
    'summary': 'Modificaciones personalizadas para lot',
    'depends': ['stock','product_expiry'],
    'data': [
        'security/grupo.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}