# -*- coding: utf-8 -*-
import requests
import json


from odoo import models, fields


class Website(models.Model):
    _inherit = 'website'

    recaptcha_site_key = fields.Char(string='ReCaptcha Site Key')
    recaptcha_private_key = fields.Char(string='ReCaptcha Private Key')

    def check_recaptcha(self, response):
        get_res = {'secret': self.recaptcha_private_key, 'response': response}
        try:
            response = requests.get(
                'https://www.google.com/recaptcha/api/siteverify', params=get_res)
        except Exception as e:
            assert 0, ('Invalid Data!, %s' % (e))
        res_con = json.loads(response.content)
        if 'success' in res_con and res_con['success']:
            return True
        return False
