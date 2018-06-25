# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2009-TODAY Odoo Peru(<http://www.bitodoo.pe>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': 'Tipo de cambio Peru',
    'version': '1.0',
    'author': 'Bitodoo',
    'category': 'Accounting',
    'summary': 'Permite ingresar tipo de cambio en formato peruano.',
    'license': 'AGPL-3',
    'contributors': [
        'Leonidas Pezo <leonidas@bitodoo.pe>',
    ],
    'description': """
Registro de tpo de cambio
-----------------------

Registra el tipo de cambio jalando de la pagina de la sunat:

    """,
    'website': 'http://bitodoo.com',
    'depends': ['account'],
    'data': [
        'views/form_view.xml',
        'data/res_currency_data.xml',
    ],
    'images': [
        'static/description/banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    "sequence": 2,
}
