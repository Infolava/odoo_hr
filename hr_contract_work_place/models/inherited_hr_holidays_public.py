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
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class hr_holidays_public(models.Model):
    _name = "hr.holidays.public"
    _inherit = "hr.holidays.public"
    
    @api.multi
    def get_public_holidays_for_countries(self, country_id, dt_from = False, dt_to = False):
        """
            Get public holidays list for a country list for specified date period
            @param dt_from : date : Start date period
            @param dt_to : date : End date period
            @param country_id: integer : country id 
            @return: list : list of public holiday line record
        """
        domain = [('country_id', '=', country_id)]
        if dt_from :
            domain.append(('year', '>=', dt_from.year))
        if dt_to :
            domain.append(('year', '<=', dt_to.year))
        official_holidays_by_country = self.search(domain)
        result = []
        for hol in official_holidays_by_country :
            result += [line for line in hol.line_ids \
                       if (not dt_from) \
                       or \
                       (dt_from  and fields.Date.from_string(line.date) >= dt_from) \
                        or \
                        (dt_to and fields.Date.from_string(line.date) <= dt_to)]
        return result
    
    @api.multi
    def get_public_holidays_for_state(self, state_id, dt_from = False, dt_to = False) :
        """
            Get public holiday for a state for specified date period
            @param dt_from : date : Start date period
            @param dt_to : date : End date period
            @param state_id: integer : state id
            @return: list : list of public holiday line record
        """
        country_id = self.env['res.country.state'].browse(state_id).country_id.id
        hol_lines = self.get_public_holidays_for_countries(country_id, dt_from, dt_to)
        return [line for line in hol_lines if (not line.state_ids or state_id in line.state_ids.ids)]

class hr_holidays_public_line(models.Model):
    _name = "hr.holidays.public.line"
    _inherit = "hr.holidays.public.line"
    
    paid = fields.Boolean('Paid', default = True)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
#eof $Id$