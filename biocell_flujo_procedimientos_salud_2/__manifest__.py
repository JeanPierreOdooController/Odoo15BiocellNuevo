# -*- coding: utf-8 -*-
{
    'name': "Grupos procedimiento clinico",
    'author': 'ITGRUPO, Alessandro Pelayo Mollocondo Medrano',
    'category': 'Others',
    'description': """Modulo que habilita los grupos para que tengan acceso dependiendo del caso""",
    'version': '1.0',
    'summary': 'Modificaciones personalizadas para procedimientos clinicos',
    'depends': ['biocell_flujo_procedimientos_salud'],
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}