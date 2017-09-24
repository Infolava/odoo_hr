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

class hr_contract(models.Model):
    _name = "hr.contract"
    _inherit = "hr.contract"
    _description = "Extend hr.contract model to update event attendees"

    @api.model
    def create(self, values):
        res = super(hr_contract, self).create(values)
        self.env['hr.holidays.public.line'].update_event_attendees([res.state_id.id])
        return res
    
    @api.multi
    def write(self, values) :
        if values.get('state_id') or values.get('employee_id') or values.get('date_start') or values.get('date_start') :
            # Update holiday related event attendees
            state_ids = self.state_id.ids + [values['state_id']] if values.get('state_id') else self.state_id.ids
            res = super(hr_contract, self).write(values)
            self.env['hr.holidays.public.line'].update_event_attendees(state_ids)
            return res
        return super(hr_contract, self).write(values)
    
    @api.multi
    def unlink(self) :
        res = super(hr_contract, self).unlink()
        self.env['hr.holidays.public.line'].update_event_attendees(self.state_id.ids)
        return res