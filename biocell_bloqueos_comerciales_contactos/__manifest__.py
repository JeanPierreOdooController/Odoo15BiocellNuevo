{
    'name': 'Restricciones perfil comercial',
    'version': '1.0',
    'summary': 'Restricciones para usuarios comerciales en biocell_directorio_contactos, plantillas de venta y listas de precios',
    'description': '''
        Este módulo implementa restricciones para usuarios comerciales en:
        
        Contactos (res.partner):
        - Restringe las opciones de archivo/desarchivar
        - Restringe la eliminación de biocell_directorio_contactos
        
        Plantillas de Venta (sale.order.template):
        - Restringe las opciones de archivo/desarchivar
        - Restringe la eliminación de plantillas
        
        Listas de Precios (product.pricelist):
        - Restringe las opciones de archivo/desarchivar
        - Restringe la eliminación de listas de precios
    ''',
    'author': 'ITGRUPO, Irving Llerena',
    'depends': ['base', 'contacts', 'sale_management', 'product'],
    'data': [
        'security/security_groups.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}