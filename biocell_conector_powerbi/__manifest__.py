# -*- encoding: utf-8 -*-
{
    'name': 'APIs PowerBI',
    'version': '1.0',
    'description': 'APIs PowerBI',
    'author': 'ITGRUPO, Jhorel Revilla',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'biocell_panel_saldos_financieros_4_lote'
    ],
    'data': [
        'data/biocell_conector_powerbi_key.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/inventory_biocell_conector_powerbi.xml',
        'views/invoice_biocell_conector_powerbi.xml',
        'views/biocell_conector_powerbi_key.xml',
        'views/sale_biocell_conector_powerbi.xml',
    ],
    'auto_install': False,
    'application': False,
}