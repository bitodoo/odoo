# -*- coding: utf-8 -*-

{
    'name': "Bitodoo product attribute",

    'summary': """Bitodoo product attribute""",

    'description': """
    # Add fields in product

    - Colección
    - Modelo
    - Composición
    - Nombre comercial
    - Temporada
    - Etc.
    """,
    'author': "Bitodoo",
    'website': "http://www.bitodoo.com",
    'category': 'Others',
    'version': '0.1',

    'depends': ['product', 'bitodoo_datas'],

    'data': [
        'views/product_views.xml',
        'data/bo.datas.csv',
    ],

    'demo': [
    ],
    'application': True,
}
