# -*- coding: utf-8 -*-

from odoo import models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if not self.env.user.has_group('stock.group_stock_manager'):
            args += [
                '|', ('location_id', 'in', self.env.user.location_ids.ids),
                ('location_dest_id', 'in', self.env.user.location_ids.ids)]
        return super(StockPicking, self).search(
            args=args, offset=offset, limit=limit, order=order, count=count)
