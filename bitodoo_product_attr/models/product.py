# -*- coding: utf-8 -*-
# © 2017 Bitodoo (<http://www.bitodoo.com>).


from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    collection_data_id = fields.Many2one(
        comodel_name='bo.datas', string=u'Colección', domain=[('parent_id.code', '=', '_collection')])
    model_data_id = fields.Many2one(
        comodel_name='bo.datas', string=u'Modelo', domain=[('parent_id.code', '=', '_model')])
    gender_data_id = fields.Many2one(
        comodel_name='bo.datas', string=u'Género', domain=[('parent_id.code', '=', '_gender')])
    composition = fields.Char(string=u'Composición')
    tradename_data_id = fields.Many2one(
        comodel_name='bo.datas', string='Nombre comercial', domain=[('parent_id.code', '=', '_tradename')])
