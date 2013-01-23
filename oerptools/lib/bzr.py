#!/usr/bin/python2
# -*- coding: utf-8 -*-
########################################################################
#
#  OpenERP Tools by CLEARCORP S.A.
#  Copyright (C) 2009-TODAY CLEARCORP S.A. (<http://clearcorp.co.cr>).
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public
#  License along with this program.  If not, see 
#  <http://www.gnu.org/licenses/>.
#
########################################################################

'''
Description: Install bzr
'''

import logging
from oerptools.lib import tools

_logger = logging.getLogger('oerptools.lib.bzr')

def bzr_install():
    os_version = tools.get_os()
    if os_version and os_version['os'] == 'Linux':
        if os_version['version'][0] == 'Ubuntu':
            return ubuntu_bzr_install()
        elif os_version['version'][0] == 'arch':
            return arch_bzr_install()
    _logger.warning('Can\'t install bzr in this OS')
    return False

def ubuntu_bzr_install():
    #TODO: logger gets the output of the command
    _logger.info('Installing bzr...')
    tools.exec_command('apt-get -y update')
    tools.exec_command('apt-get -y install bzr python-bzrlib')
    return

def arch_bzr_install():
    #TODO: logger gets the output of the command
    _logger.info('Installing bzr...')
    tools.exec_command('pacman -Sy --noconfirm bzr')
    return

def bzr_initialize():
    _logger.debug('Importing and initializing bzrlib')
    from bzrlib.branch import Branch
    from bzrlib.trace import set_verbosity_level
    from bzrlib.plugin import load_plugins
    from bzrlib import initialize
    library_state = initialize()
    library_state.__enter__()
    set_verbosity_level(1000)
    
    import oerptools.lib.logger
    oerptools.lib.logger.set_levels()