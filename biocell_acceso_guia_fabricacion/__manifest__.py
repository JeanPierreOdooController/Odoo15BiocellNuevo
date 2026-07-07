{
    'name': 'Albaran agregar botón mrp',
    'version': '1.0',
    'description': 'Albaran agregar botón mrp',
    'author': 'ITGRUPO',
    'license': 'LGPL-3',
    'category': 'Sumtec',
    'auto_install': False,
    'depends': [
    #     'sale',
    #     'project',
    #     'account'
        'biocell_panel_saldos_financieros_4','biocell_panel_saldos_financieros_4_lote','mrp','stock','biocell_acceso_guia_operacion'
    ],
    'data': [
        'views/ir.model.access.csv',
        'views/button.xml',
    ],
    'installable': True
}