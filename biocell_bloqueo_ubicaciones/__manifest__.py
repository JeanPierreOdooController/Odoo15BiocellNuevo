# -*- coding: utf-8 -*-
{
    'name': 'Restricción de Ubicación para Cambios de Lote',
    'version': '15.0.1.0.0',
    'author': 'ITGRUPO',
    'website': '',
    'category': 'stock',
    'description':
        """
        Restricción de Ubicación para Cambios de Lote
        
        Este módulo permite:
        - Marcar ubicaciones como bloqueadas para un grupo específico
        - Restringir la creación, eliminación y edición de pickings cuando 
          la ubicación de origen o destino está marcada como bloqueada
        """,
    'depends': ['stock', 'base'],
    'data': [
        'security/groups.xml',
        'views/stock_location_views.xml',
    ],
    'auto_install': False,
    'installable': True
}

