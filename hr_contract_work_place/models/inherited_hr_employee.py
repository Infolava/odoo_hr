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
# Created:               Aug 14, 2017 11:09:55 AM by hbouzidi
# Last modified:      2017-08-14 11:09
#
# Last Author:           $LastChangedBy$
# Last Checkin:          $LastChangedDate$
# Checked out Version:   $LastChangedRevision$
# HeadURL:               $HeadURL$
# --------------------------------------------------------------------------------
from openerp import models, api, _
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class hr_employee(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"
    
    @api.multi
    def _get_official_holidays_by_contracts(self, dt_st, dt_end):
        public_hol = []
        for contract in self.contract_ids:
            public_hol += self.env['hr.holidays.public'].get_public_holidays_for_state(dt_st, dt_end, contract.state_id.id)
        return public_hol
        
    @api.multi
    def _compute_public_holidays(self, dt_from, dt_until): 
        """
            compute total working hours of public holidays
            @param dt_from: datetime, starting date
            @param dt_from: datetime, ending date
            @return: float
        """
        hours = 0.0
        off_hol_dates = [pub_hol.date for pub_hol in self._get_official_holidays_by_contracts(dt_from, dt_until)]
        while dt_from <= dt_until:
            date_from = dt_from.date()
            date_from = date_from.strftime(DF)
            if date_from in off_hol_dates :
                hours += self._get_total_working_hours(dt_from)
            dt_from = dt_from + timedelta(days=1)
        return hours
            
        