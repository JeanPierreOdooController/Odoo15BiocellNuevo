# -*- coding: utf-8 -*-
{
    'name': "Vehiculo por defectp",
    'author': 'ITGRUPO, Alessandro Pelayo Mollocondo Medrano',
    'category': 'Fleet',
    'description': """Modulo que genera que un vehiculo sea por defecto y que tambien solo sea uno el cual tenga este check marcado""",
    'version': '1.0',
    'summary': 'Modificaciones personalizadas para fleet',
    'depends': ['fleet','stock','biocell_extensiones_contables','biocell_pe_facturacion_electronica','biocell_logistica_operativa'],
    'data': [
        'views/agregar.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}