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
from openerp import models, api, _, fields
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
    
class hr_holidays_public_line(models.Model):
    _name = "hr.holidays.public.line"
    _inherit = "hr.holidays.public.line"
    
    event_id = fields.Many2one('calendar.event', string = 'Related event', readonly = True, ondelete = 'cascade')

    @api.multi
    def update_holiday_event_attendees(self, state_ids):
        for hol in self :
            for st_id in state_ids :
                contracts = self.env['hr.contract'].search([
                                                            ('state_id', '=', st_id), \
                                                            ('date_start', '<=', fields.Datetime.from_string(hol.date)), \
                                                            '|',
                                                            ('date_end', '=', False), \
                                                            ('date_end', '>=', fields.Datetime.from_string(hol.date))])
                hol.event_id.with_context(no_email = True).partner_ids = [[6, False, [contract.employee_id.user_id.partner_id.id for contract in contracts]]]
        
    @api.model
    def update_event_attendees(self, state_ids):
        for state_id in state_ids :
            contracts = self.env['hr.contract'].search([('state_id', '=', state_id)])
            holidays = self.env['hr.holidays.public'].get_public_holidays_for_state(state_id)
            for hol in holidays :
                hol.event_id.with_context(no_email = True).partner_ids = [[6, False, []]]
            for contract in contracts :
                holidays = self.env['hr.holidays.public'].get_public_holidays_for_state(contract.state_id.id, \
                                                                                        fields.Datetime.from_string(contract.date_start), \
                                                                                        fields.Datetime.from_string(contract.date_end) or False, \
                                                                                        )
                for hol in holidays :
                    hol.event_id.with_context(no_email = True).partner_ids = [(4, contract.employee_id.user_id.partner_id.id)]
            
    @api.model
    def create(self, values):
        meeting_vals = {}
        if values.has_key('date') and values['date'] is not False:
            meeting_vals.update({'start_date': values['date'], 'stop_date': values['date']})
            if type(values['date']) is datetime :
                meeting_vals.update({'start_date': (values['date'].date()).strftime(DF), 'stop_date': (values['date'].date()).strftime(DF)})

        meeting_vals.update({
                             'name': values['name'] or _('Official Holiday'),
                             'duration': 24,
                             'state': 'open',
                             'class': 'confidential',
                             'allday' : True,
                             'partner_ids' : [[6, False, []]]
                             })
        country = self.env['hr.holidays.public'].browse(values['year_id']).country_id
        if not values.has_key('state_ids') or not values['state_ids'] or not values['state_ids'][0][2] :
            state_ids = self.env['res.country.state'].search([('country_id', '=', country.id)]).ids
        else :
            state_ids = values['state_ids'][0][2]
            
        values['event_id'] = self.env['calendar.event'].with_context(no_email = True).create(meeting_vals).id
        holiday = super(hr_holidays_public_line, self).create(values)
        holiday.update_holiday_event_attendees(state_ids)
        return holiday

    @api.multi
    def unlink(self):
        for hol in self :
            hol.event_id.with_context(no_email = True).unlink()
        return super(hr_holidays_public_line, self).unlink()
    
    @api.multi
    def write(self, values):
        related_event = self.env['calendar.event'].browse(self.event_id.ids)
        res = super(hr_holidays_public_line, self).write(values)
        vals = {}
        if values.has_key('date') and  values['date'] is not False:
            vals.update({'start_date': values['date'], 'stop_date' : values['date']})
            if type(values['date']) is datetime :
                vals.update({'start_date': (values['date'].date()).strftime(DF), 'stop_date': (values['date'].date()).strftime(DF)})
        if values.has_key('name') and  values['name'] is not False :
            vals.update({'name': values['name']})
        if self._uid !=  related_event.user_id.id :
            vals.update({'user_id': self._uid})
        for hol in self :
            hol.event_id.with_context(no_email = True).write(vals)
            
            if values.has_key('state_ids') :
                if not values['state_ids'] or not values['state_ids'][0][2]:
                    state_ids = self.env['res.country.state'].search([('country_id', '=', hol.year_id.country_id.id)]).ids
                else :
                    state_ids = values['state_ids'][0][2]
                self.update_holiday_event_attendees(state_ids)
        return res
