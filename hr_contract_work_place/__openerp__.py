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
# Created:               Aug 11, 2017 9:41:56 AM by hbouzidi
# Last modified:      2017-08-11 09:41
#
# Last Author:           $LastChangedBy$
# Last Checkin:          $LastChangedDate$
# Checked out Version:   $LastChangedRevision$
# HeadURL:               $HeadURL$
# --------------------------------------------------------------------------------
{
    'name' : 'Contract By state',
    'version' : '2.0.2',
    'author' : 'Infolava',
    'website': 'http://www.infolava.ch',
    'category' : 'Human Ressources Management',
    'depends' : [
                 'hr_contract',
                 'hr_public_holidays',
                 ],
    'demo_xml' : [],
    'summary': "Addon to manage employee's contracts by state",
    'data' : [
              'views/inherited_hr_contract_form_view.xml',
              'views/inherieted_hr_holidays_public.xml',
              ],
    'active': False,
    'installable': True,
    'application' : True,
}
