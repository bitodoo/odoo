from odoo import api, fields, models


class BODatas(models.Model):
    _name = 'bo.datas'
    _description = 'Bitodoo datas'
    _order = 'parent_id, sequence, name'
    _description = 'Bitooo datas'

    def _default_parent_id(self):
        _code = self.env.context.get('code')
        parent = self.search([('code', '=', _code), ('parent_id', '=', False)], limit=1)
        return parent.id

    parent_id = fields.Many2one('bo.datas', string='Parent', ondelete='cascade', default=_default_parent_id)
    name = fields.Char('Name', size=100, required=True)
    code = fields.Char('Code', size=50)
    alias = fields.Char('Abbreviation', size=30)
    value_1 = fields.Char('Value 1')
    value_2 = fields.Char('Value 2')
    value_3 = fields.Char('Value 3')
    active = fields.Boolean('Activo/Inactivo', default=True)
    child_ids = fields.One2many('bo.datas', 'parent_id', 'Items')
    sequence = fields.Integer(default=10)

    @api.model
    def get_values(self, parent_code, key='code'):
        domain = [('parent_id.code', '=', parent_code)]
        return [(getattr(obj, key), obj.name) for obj in self.search(domain)]
