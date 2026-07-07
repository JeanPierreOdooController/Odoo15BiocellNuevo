# -*- enconding:utf-8 -*-
{
    'name': 'Agregar Campos al Reporte de "Operaciones de Albaran"',
    'version': '1.0',
    'description': 'Modulo que agrega los campos "Nombre del Paciente", "Centro Medico" y "Nombre del Doctor" al reporte de "Operaciones de Albaran".',
    'author': 'ITGRUPO, Jhorel Revilla Calderon',
    'license': 'LGPL-3',
    'depends': [
        'stock'
    ],
    'data': [
        'views/report_picking_inherit.xml'
    ],
    'auto_install': False,
    'application': False
}