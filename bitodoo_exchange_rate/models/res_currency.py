# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools
from . import pe_exchange_rate

TYPES = [('purchase', 'Compra'), ('sale', 'Venta')]


class Currency(models.Model):
    _inherit = "res.currency"
    _description = "Currency"

    rate_pe = fields.Float(
        compute='_compute_current_rate_pe',
        string='Cambio del día',
        digits=(12, 4),
        help='Tipo de cambio del dia en formato peruano.'
    )
    type = fields.Selection(
        TYPES,
        required=True,
        string='Tipo',
        default='sale'
    )

    @api.multi
    def action_exchange_rate_sale(self):
        obj_rcr_ids = self.env['res.currency.rate']
        if self.type == "sale" and self.symbol.upper() == "$":
            create = obj_rcr_ids.create({
                'currency_id': self.id,
                'date': fields.Date.today(),
                'rate_pe': pe_exchange_rate.exchange_rate_sale(self)
            })
            return create
        if self.type == "purchase" and self.symbol.upper() == "$":
            create = obj_rcr_ids.create({
                'currency_id': self.id,
                'date': fields.Date.today(),
                'rate_pe': pe_exchange_rate.exchange_rate_purchase(self)
            })
            return create

    @api.multi
    def _compute_current_rate_pe(self):
        date = self._context.get('date') or fields.Date.today()
        company_id = self._context.get('company_id') or self.env['res.users']._get_company().id
        query = """SELECT c.id, (SELECT r.rate_pe FROM res_currency_rate r
                                  WHERE r.currency_id = c.id AND r.name <= %s
                                    AND (r.company_id IS NULL OR r.company_id = %s)
                               ORDER BY r.company_id, r.name DESC
                                  LIMIT 1) AS rate_pe
                   FROM res_currency c
                   WHERE c.id IN %s"""
        self._cr.execute(query, (date, company_id, tuple(self.ids)))
        currency_rates = dict(self._cr.fetchall())
        for currency in self:
            currency.rate_pe = currency_rates.get(currency.id) or 1.0

    @api.multi
    def name_get(self):
        return [(currency.id, tools.ustr(currency.name + ' - ' + dict(TYPES)[currency.type])) for currency in self]

    _sql_constraints = [
        ('unique_name', 'unique (name,type)', 'Solo puede existir una moneda con el mismo tipo de cambio!'),
        ('rounding_gt_zero', 'CHECK (rounding>0)', 'The rounding factor must be greater than 0!')
    ]


class CurrencyRate(models.Model):
    _inherit = "res.currency.rate"
    _description = "Currency Rate"

    rate_pe = fields.Float(
        string='Cambio',
        digits=(12, 4),
        help='Tipo de cambio en formato peruano. Ejm: 3.25 si $1 = S/. 3.25'
    )
    type = fields.Selection(related="currency_id.type", store=True)

    @api.onchange('rate_pe')
    def onchange_rate_pe(self):
        if self.rate_pe > 0:
            self.rate = 1 / self.rate_pe
