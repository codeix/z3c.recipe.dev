##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Z3c development recipes

$Id:$
"""

import os, sys, shutil
import zc.buildout
import zc.recipe.egg
import pkg_resources
import ZConfig.schemaless
import cStringIO


class ScriptSetup:

    def __init__(self, buildout, name, options):
        self.egg = None
        self.buildout = buildout
        self.name = name
        self.options = options
        options['script'] = os.path.join(buildout['buildout']['bin-directory'],
                                         options.get('script', self.name),
                                         )
        if not options.get('working-directory', ''):
            options['location'] = os.path.join(
                buildout['buildout']['parts-directory'], name)

        if options.get('eggs'):
            self.egg = zc.recipe.egg.Egg(buildout, name, options)

    def install(self):
        options = self.options
        module = options['module']
        method = options.get('method', 'py')
        executable = self.buildout['buildout']['executable']

        # setup additional egg path
        if self.egg:
            extra_paths = self.egg.extra_paths
            eggs, ws = self.egg.working_set()
        else:
            extra_paths = ()
            ws = []

        # setup script default vars
        arguments = options.get('arguments', '').strip()

        wd = options.get('working-directory', options['location'])

        # setup environment
        initialization = initialization_template
        env_section = self.options.get('environment', '').strip()
        if env_section:
            env = self.buildout[env_section]
            for key, value in env.items():
                initialization += env_template % (key, value)

        return zc.buildout.easy_install.scripts(
            [(options['script'], module, method)],
            ws, executable, self.buildout['buildout']['bin-directory'],
            extra_paths = extra_paths,
            arguments = arguments,
            initialization = initialization,
            )

        return ()

    update = install


initialization_template = """import os
sys.argv[0] = os.path.abspath(sys.argv[0])
"""

env_template = """os.environ['%s'] = %r
"""
