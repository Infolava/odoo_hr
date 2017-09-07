# -*- encoding: utf-8 -*-
# --------------------------------------------------------------------------------
# Project:               TransALM
# Copyright:           © 2017 Infolava GmbH. All rights reserved.
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
# Created:               Sep 7, 2017 11:58:56 AM by atrabelsi
# Last modified:      2017-09-07 11:58
#
# Last Author:           $LastChangedBy$
# Last Checkin:          $LastChangedDate$
# Checked out Version:   $LastChangedRevision$
# HeadURL:               $HeadURL$
# --------------------------------------------------------------------------------

from openerp import models, api, fields, _ 
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class hr_holidays_public(models.Model):
    _name = "hr.holidays.public"
    _inherit = "hr.holidays.public"
    
    @api.multi
    def get_public_holidays_for_countries(self, dt_from, dt_to, country_id):
        """
            Get public holidays list for a country list for specified date period
            @param dt_from : date : Start date period
            @param dt_to : date : End date period
            @param country_id: integer : country id 
            @return: list : list of public holiday line record
        """
        official_holidays_by_country = self.search([('country_id', '=', country_id),
                                                    ('year', '>=', dt_from.year), 
                                                    ('year', '<=', dt_to.year)])
        return [line for line in official_holidays_by_country.line_ids \
                if (fields.Datetime.from_string(line.date) >= dt_from \
                    or \
                    fields.Datetime.from_string(line.date) <= dt_to)]
    
    @api.multi
    def get_public_holidays_for_state(self, dt_from, dt_to, state_id) :
        """
            Get public holiday for a state for specified date period
            @param dt_from : date : Start date period
            @param dt_to : date : End date period
            @param state_ids: integer : state id
            @return: list : list of public holiday line record
        """
        country_id = self.env['res.country.state'].browse(state_id).country_id.id
        hol_lines = self.get_public_holidays_for_countries(dt_from, dt_to, country_id)
        return [line for line in hol_lines if (not line.state_ids or state_id in line.state_ids.ids)]
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
#eof $Id$