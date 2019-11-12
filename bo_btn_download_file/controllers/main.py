from odoo.tools import html_escape
import json

from odoo import http
from odoo.http import content_disposition, request
from odoo.addons.web.controllers.main import serialize_exception


class Binary(http.Controller):
    @http.route('/web/download/binary_content', type='http', auth="public")
    @serialize_exception
    def download_binary_content(self, model, method, id, filename='download_file.xls',
                                mimetype='application/octet-stream;charset=utf-8;', **kw):
        id = int(id)
        if not model or not method or not id or not filename or not mimetype:
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': "Not params"}
            return request.make_response(html_escape(json.dumps(error)))

        if not request.env['ir.model'].sudo().search([('model', '=', model)]):
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': "Not exist model"}
            return request.make_response(html_escape(json.dumps(error)))
        Model = request.env[model]
        if not hasattr(Model, method):
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': "Not method"}
            return request.make_response(html_escape(json.dumps(error)))

        data = getattr(Model.sudo().browse(id), method)()

        headers = [
            ('Content-Type', mimetype),
            ('Content-Length', len(data)),
            ('Content-Disposition', content_disposition(filename))
        ]

        return request.make_response(data, headers=headers)
