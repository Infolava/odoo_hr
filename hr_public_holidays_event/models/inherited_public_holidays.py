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
# Created:               Aug 11, 2017 10:37:04 AM by hbouzidi
# Last modified:      2017-08-11 10:37
#
# Last Author:           $LastChangedBy$
# Last Checkin:          $LastChangedDate$
# Checked out Version:   $LastChangedRevision$
# HeadURL:               $HeadURL$
# --------------------------------------------------------------------------------
from openerp import models, api, _ 
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class hr_holidays_public(models.Model):
    _name = "hr.holidays.public"
    _inherit = "hr.holidays.public"
    
    @api.multi
    def get_public_holidays_for_state(self, dt_from, dt_to, state_id):
        return [self.env['hr.holidays.public.line'].search([('state_ids', 'in', [state_id.id]), ('date', '>=', dt_from), ('date', '<=', dt_to)])]

    @api.multi
    def get_public_holidays_for_country(self,dt_from, dt_to, countries_ids):
        """
        Get public holidays line for a country without specific state
        """
        official_holidays_by_country = self.env['hr.holidays.public'].search([('country_id', 'in', countries_ids),('year', '>=', dt_from.year), ('year', '<=', dt_to.year)])
        pub_hol_country_line = []
        for pub_hol_count in official_holidays_by_country :
            pub_hol_count_lines_ids = [line.id for line in pub_hol_count.line_ids]
            pub_hol_country_line += self.env['hr.holidays.public.line'].search([('id', 'in',pub_hol_count_lines_ids), ('state_ids', '=', False), ('date', '>=', dt_from), ('date', '<=', dt_to)])
        return pub_hol_country_line
        
class hr_holidays_public_line(models.Model):
    _name = "hr.holidays.public.line"
    _inherit = "hr.holidays.public.line"
    
    @api.model
    def create(self, values):
        meeting_vals = {}
        if values.has_key('date') and  values['date'] is not False:
            meeting_vals.update({'start': values['date'], 'stop': values['date']})
            if type(values['date']) is datetime :
                meeting_vals.update({'start': (values['date'].date()).strftime(DF), 'stop': (values['date'].date()).strftime(DF)})
        meeting_vals.update({
                    'name': values['name'] or _('Official Holiday'),
                    'duration': 24,
                    'state': 'open',
                    'class': 'confidential'
                })
        self.env['calendar.event'].create(meeting_vals)
        return super(hr_holidays_public_line, self).create(values)
    
    @api.multi
    def unlink(self):
        related_event = self.env['calendar.event'].search([('name', "=", self.name), ('start', '=', self.date), ('stop', '=', self.date)])
        res = super(hr_holidays_public_line, self).unlink()
        related_event.unlink()
        return res
    
    @api.multi
    def write(self, values):
        related_event = self.env['calendar.event'].search([('name', "=", self.name), ('start', '=', self.date), ('stop', '=', self.date)])
        vals = {}
        if values.has_key('date') and  values['date'] is not False:
            vals .update({'start': values['date'], 'stop' : values['date']})
        if values.has_key('name') and  values['name'] is not False :
            vals.update({'name': values['name']})
        if self._uid !=  related_event.user_id :
            vals.update({'user_id': self._uid})
        res = super(hr_holidays_public_line, self).write(values)
        related_event.write(vals)
        return res
        
         
