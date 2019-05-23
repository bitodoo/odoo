from odoo import models, api, _
from odoo.exceptions import UserError


class IrActionsActUrl(models.Model):
    _inherit = 'ir.actions.act_url'

    @api.model
    def binary_content(self, model=False,
                       # Method return base64
                       method=False,
                       id=False,
                       filename='download_file.xls',
                       mimetype='application/octet-stream'):

        if not model or not method or not id or not filename or not mimetype:
            raise UserError(_(u"Not param"))
        if not self.env['ir.model'].search([('model', '=', model)]):
            raise UserError(_(u"Not found model"))
        m = self.env[model]
        if not hasattr(m, method):
            raise UserError(_(u"Not found method"))
        values = {
            'model': model,
            'method': method,
            'id': id,
            'filename': filename,
            'mimetype': mimetype
        }
        url = '/web/download/binary_content?model={model}&method={method}&id={id}&filename={filename}&mimetype={mimetype}'

        return {
            'type': 'ir.actions.act_url',
            'url': url.format(**values),
            'target': 'download'}
