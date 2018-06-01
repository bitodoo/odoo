# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import Warning


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_assign(self):
        location_origin_names = [x.location_id.name for x in self.move_lines if x.location_id.id != self.location_id.id]
        location_dest_names = [x.location_dest_id.name for x in self.move_lines if x.location_dest_id.id != self.location_dest_id.id]
        if location_origin_names:
            msm = u"las ubicaciones de origén [{}] son diferentes a la ubicación de la transferencia ({})"
            raise Warning(msm.format(', '.join(location_origin_names), self.location_id.name))
        if location_dest_names:
            msm = u"las ubicaciones [{}] son diferentes a la ubicación de la transferencia ({})"
            raise Warning(msm.format(', '.join(location_dest_names), self.location_dest_id.name))
        res = super(StockPicking, self).action_assign()
        return res
