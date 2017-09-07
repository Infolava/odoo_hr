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
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
    
class hr_holidays_public_line(models.Model):
    _name = "hr.holidays.public.line"
    _inherit = "hr.holidays.public.line"
    
#     @api.multi
#     def _get_attendees(self, state_ids):
#         """
#         attendees are related partner for employees according to their contract state
#         """
#         contract_ids = self.env['hr.contract'].search([('state_id', 'in', [state_id.id for state_id in state_ids])])
#         employee_ids = self.env['hr.employee'].search([('contract_ids', 'in',[contract_id.id for contract_id in contract_ids])])
#         user_ids = self.env['res.users'].search([('employee_ids', 'in', [employee_id.id for employee_id in employee_ids])])
#         return self.env['res.partner'].search([('user_ids', 'in', [user_id.id for user_id in user_ids])])
    
    @api.model
    def create(self, values):
        meeting_vals = {}
        if values.has_key('date') and  values['date'] is not False:
            meeting_vals.update({'start_date': values['date'], 'stop_date': values['date']})
            if type(values['date']) is datetime :
                meeting_vals.update({'start_date': (values['date'].date()).strftime(DF), 'stop_date': (values['date'].date()).strftime(DF)})
        meeting_vals.update({
                    'name': values['name'] or _('Official Holiday'),
                    'duration': 24,
                    'state': 'open',
                    'class': 'confidential',
                    'partner_ids' : [self._uid],
                    'allday' : True,
                })
        res = super(hr_holidays_public_line, self).create(values)
        if values['state_ids'] is False :
            state_ids = self.env['res.country.state'].search([('country_id', '=', res.year_id.country_id.id)])
#         for partner in self._get_attendees(state_ids) :
#             meeting_vals['partner_ids'] += [(4,partner.id)]
                    
        ctx_no_email = dict(self._context or {}, no_email=True)
        self.env['calendar.event'].create(meeting_vals, context=ctx_no_email)
        return res
    
    @api.multi
    def unlink(self):
        related_event = self.env['calendar.event'].search([('name', "=", self.name), ('start_date', '=', self.date), ('stop_date', '=', self.date)])
        res = super(hr_holidays_public_line, self).unlink()
        related_event.unlink()
        return res
    
    @api.multi
    def write(self, values):
        related_event = self.env['calendar.event'].search([('name', "=", self.name), ('start_date', '=', self.date), ('stop_date', '=', self.date)])
        vals = {}
        if values.has_key('date') and  values['date'] is not False:
            vals.update({'start_date': values['date'], 'stop_date' : values['date']})
        if values.has_key('name') and  values['name'] is not False :
            vals.update({'name': values['name']})
        if self._uid !=  related_event.user_id :
            vals.update({'user_id': self._uid})
        related_event.write(vals)
        return super(hr_holidays_public_line, self).write(values)
        
         
