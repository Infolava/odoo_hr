# -*- encoding: utf-8 -*-
# --------------------------------------------------------------------------------
# Project:               TransALM
# Copyright:           © 2017 All rights reserved.
# License:
# --------------------------------------------------------------------------------
#    This file is part of TransALM
#
#    TransALM is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------
# Created:               Aug 11, 2017 9:44:47 AM by hbouzidi
# Last modified:      2017-08-11 09:44
#
# Last Author:           $LastChangedBy$
# Last Checkin:          $LastChangedDate$
# Checked out Version:   $LastChangedRevision$
# HeadURL:               $HeadURL$
# --------------------------------------------------------------------------------
from openerp import models, fields, api
from openerp.exceptions import MissingError

class hr_contract(models.Model):
    _name = "hr.contract"
    _inherit = "hr.contract"
    
    state_id =  fields.Many2one('res.country.state', 'state')
    
    @api.onchange('state_id', 'date_start', 'date_end')
    def onchange_state(self) :
        if not self.date_start or not self.state_id :
            return {}
        year_start = fields.Date.from_string(self.date_start).year
        year_end = fields.Date.from_string(self.date_end).year if self.date_end else year_start + 1
        providers = self.env['calendar.provider'].search([])
        if not providers :
            raise MissingError(_("Please contact your administration to configure the calendar provider"))
        self.env['hr.holidays.public'].import_public_holidays_by_country(providers[0], \
                                                                         self.state_id.country_id, \
                                                                         year_start, \
                                                                         year_end)