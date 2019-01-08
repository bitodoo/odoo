# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import AccessDenied


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _default_website(self):
        return self.env['website'].search([], limit=1)

    # FIXME: Set website_id to ondelete='cascade' in master
    recaptcha_site_key = fields.Char('ReCaptcha Site Key', related='website_id.recaptcha_site_key')
    recaptcha_private_key = fields.Char('ReCaptcha Private Key', related='website_id.recaptcha_private_key')

    # Set as global config parameter since methods using it are not website-aware. To be changed
    # when multi-website is implemented
    has_google_recaptcha = fields.Boolean("Google Recaptcha")

    @api.onchange('has_google_recaptcha')
    def onchange_has_google_recaptcha(self):
        if not self.has_google_recaptcha:
            self.recaptcha_site_key = False
            self.recaptcha_private_key = False

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(has_google_recaptcha=get_param('bo_website_base_recaptcha.has_google_recaptcha'))
        return res

    def set_values(self):
        if not self.user_has_groups('website.group_website_designer'):
            raise AccessDenied()
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('bo_website_base_recaptcha.has_google_recaptcha', self.has_google_recaptcha)
