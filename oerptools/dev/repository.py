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

import logging
_logger = logging.getLogger('oerptools.dev.repository')

import os

from oerptools.lib import config, bzr, tools

class repository(object):
    def __init__(self):
        _logger.info('Initializing OpenERP development repository.')
        self._repo_dir = os.path.expanduser(config.params['repo_dir'] or '~/Development/openerp')
        self._no_trees = config.params['no_trees'] or False
        self._push = config.params['push'] or False
        self._repo_exists = False
        
        if os.path.isdir(self._repo_dir):
            _logger.info('Repository exists in: %s.' % self._repo_dir)
            _logger.info('Using existing repo.')
            self._repo_exists = True
        else:
            _logger.info('New repository in: %s.' % self._repo_dir)
        return super(repository, self).__init__()
    
    def _branch_project(self, name, ccorp, branches):
        _logger.info('Creating development repository for %s, branches: %s.' % (name, branches))
        
        project_dir = os.path.abspath(self._repo_dir) + '/%s' % name
        
        if os.path.isdir(project_dir):
            _logger.warning('Repository in %s already exists, delete before running the script to recreate.' % name)
        else:
            if not bzr.bzr_init_repo(project_dir, self._no_trees):
                _logger.error('Failed to create repo in %s. Exiting.' % name)
                return False
        
        if not os.path.isdir('%s/main' % project_dir):
            os.mkdir('%s/main' % project_dir)
        if not os.path.isdir('%s/features' % project_dir):
            os.mkdir('%s/features' % project_dir)
        
        for branch in branches:
            official_branch = 'lp:%s/%s' % (name, branch)
            ccorp_branch = 'lp:~clearcorp-drivers/%s/%s-ccorp' % (name, branch)
            _logger.info('Creating branches for %s/%s.' % (name, branch))
            
            _logger.info('Branch: %s.' % official_branch)
            
            if os.path.isdir('%s/main/%s/.bzr' % (project_dir, branch)):
                _logger.warning('%s/main/%s already exists, delete before running the script to recreate.' % (project_dir, branch))
            else:
                bzr.bzr_branch(official_branch, '%s/main/%s' % (project_dir, branch))
            
            if ccorp:
                _logger.info('Branch: %s.' % ccorp_branch)
                
                if os.path.isdir('%s/main/%s-ccorp/.bzr' % (project_dir, branch)):
                    _logger.warning('%s/main/%s-ccorp already exists, delete before running the script to recreate.' % (project_dir, branch))
                else:
                    bzr.bzr_branch(ccorp_branch, '%s/main/%s-ccorp' % (project_dir, branch))
            
            _logger.info('Updating parent locations for %s.' % name)
            bzr.bzr_set_parent('%s/main/%s' % (project_dir, branch), official_branch)
            bzr.bzr_set_push_location('%s/main/%s' % (project_dir, branch), official_branch)
            if ccorp:
                bzr.bzr_set_parent('%s/main/%s-ccorp' % (project_dir, branch), official_branch)
                bzr.bzr_set_push_location('%s/main/%s-ccorp' % (project_dir, branch), ccorp_branch)
            
        return True
    
    def _update_project(self, name, ccorp, branches):
        _logger.info('Updating development repository for %s, branches: %s.' % (name, branches))
        
        project_dir = os.path.abspath(self._repo_dir) + '/%s' % name
        
        if not os.path.isdir(project_dir):
            _logger.error('Repository %s doesn\'t exists. Exiting.' % name)
            return False
        
        for branch in branches:
            _logger.info('Updating %s/%s.' % (name, branch))
            
            if not os.path.isdir('%s/main/%s' % (project_dir, branch)):
                _logger.warning('Branch %s/%s doesn\'t exists. Skipping.' % (name, branch))
            else:
                if bzr.bzr_pull('%s/main/%s' % (project_dir, branch)):
                    _logger.info('Pull OK: %s/%s.' % (name, branch))
                else:
                    _logger.error('Pull ERROR: %s/%s.' % (name, branch))
            
            if ccorp:
                if not os.path.isdir('%s/main/%s-ccorp' % (project_dir, branch)):
                    _logger.warning('Branch %s/%s-ccorp doesn\'t exists. Skipping.' % (name, branch))
                else:
                    if bzr.bzr_pull('%s/main/%s-ccorp' % (project_dir, branch)):
                        _logger.info('Pull OK: %s/%s-ccorp.' % (name, branch))
                    else:
                        _logger.error('Pull ERROR: %s/%s-ccorp.' % (name, branch))
                    
                    if bzr.bzr_pull('%s/main/%s-ccorp' % (project_dir, branch), bzr.bzr_get_push_location('%s/main/%s-ccorp' % (project_dir, branch))):
                        _logger.info('Pull :push OK: %s/%s-ccorp.' % (name, branch))
                    else:
                        _logger.error('Pull :push ERROR: %s/%s-ccorp.' % (name, branch))
                    
                    if self._push:
                        if bzr.bzr_push('%s/main/%s-ccorp' % (project_dir, branch)):
                            _logger.info('Push OK: %s/%s-ccorp.' % (name, branch))
                        else:
                            _logger.error('Push ERROR: %s/%s-ccorp.' % (name, branch))
            else:
                if self._push:
                    if bzr.bzr_push('%s/main/%s' % (project_dir, branch)):
                        _logger.info('Push OK: %s/%s.' % (name, branch))
                    else:
                        _logger.error('Push ERROR: %s/%s.' % (name, branch))
        return True
    
    def make(self):
        bzr.bzr_initialize()
        _logger.info('Making new OpenERP development repository.')
        if self._repo_exists:
            _logger.info('Repository exists in: %s. Exiting.' % self._repo_dir)
            return False
        
        self._branch_project('openobject-server',     True,  ['5.0', '6.0', '6.1', '7.0', 'trunk'])
        self._branch_project('openobject-addons',     True,  ['5.0', '6.0', '6.1', '7.0', 'trunk', 'extra-5.0', 'extra-6.0', 'extra-trunk'])
        self._branch_project('openobject-client',     True,  ['5.0', '6.0', '6.1', 'trunk'])
        self._branch_project('openobject-client-web', True,  ['5.0', '6.0', 'trunk'])
        self._branch_project('openerp-web',           True,  ['6.1', '7.0', 'trunk'])
        self._branch_project('openobject-doc',        True,  ['5.0', '6.0', '6.1'])
        
        self._branch_project('openerp-ccorp-addons',  False, ['5.0', '6.0', '6.1', '7.0', 'trunk'])
        self._branch_project('openerp-costa-rica',    False, ['5.0', '6.0', '6.1', '7.0', 'trunk'])
        self._branch_project('oerptools',             False, ['stable', '1.0', '2.0', 'trunk'])
        
        self._branch_project('banking-addons',        True,  ['5.0', '6.0', '6.1', '7.0', 'trunk'])
        
        return True
    
    def update(self):
        bzr.bzr_initialize()
        _logger.info('Updating OpenERP development repository.')
        if not self._repo_exists:
            _logger.info('Repository doesn\'t exist in: %s. Exiting.' % self._repo_dir)
            return False
        
        self._update_project('openobject-server',     True,  ['5.0', '6.0', '6.1', '7.0', 'trunk'])
        self._update_project('openobject-addons',     True,  ['5.0', '6.0', '6.1', '7.0', 'trunk', 'extra-5.0', 'extra-6.0', 'extra-trunk'])
        self._update_project('openobject-client',     True,  ['5.0', '6.0', '6.1', 'trunk'])
        self._update_project('openobject-client-web', True,  ['5.0', '6.0', 'trunk'])
        self._update_project('openerp-web',           True,  ['6.1', '7.0', 'trunk'])
        self._update_project('openobject-doc',        True,  ['5.0', '6.0', '6.1'])
        
        self._update_project('openerp-ccorp-addons',  False, ['5.0', '6.0', '6.1', '7.0', 'trunk'])
        self._update_project('openerp-costa-rica',    False, ['5.0', '6.0', '6.1', '7.0', 'trunk'])
        self._update_project('oerptools',             False, ['stable', '1.0', '2.0', 'trunk'])
        
        self._update_project('banking-addons',        True,  ['5.0', '6.0', '6.1', '7.0', 'trunk'])
        
        return True