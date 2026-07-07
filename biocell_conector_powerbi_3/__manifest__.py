#-*- encoding: utf-8 -*-
{
    'name': 'Datos de Powerbi-Sale Order',
    'version': '1.0',
    'description': 'Tabla para el PowerBi',
    'author': 'ITGRUPO, Jhorel Revilla Calderon',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'mail'
    ],
    'data':[
        'security/ir.model.access.csv',
        'wizard/biocell_conector_powerbi_3_wizard_views.xml',
        'views/biocell_conector_powerbi_3.xml'
    ],
    'auto_install': False,
    'application': False
}