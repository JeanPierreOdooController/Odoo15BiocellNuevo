{
    'name': 'Consulta RUC-SUNAT',
    'version': '1.0',
    'description': 'Permite consultar RUC desde SUNAT',
    'author': 'ITGRUPO, Jhorel Revilla Calderon, Sebastian Moises Loraico Lopez',
    'license': 'LGPL-3',
    'category': 'base',
    'depends': [
        'base', 'biocell_consulta_identidad_peru'
    ],
    'data': [ 
        'data/attachment_sample.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/biocell_validador_padron_tributario_2.xml',
        'wizard/query_ruc_sunat_wizard_it.xml'
    ],
    'auto_install': False,
    'application': True,
}