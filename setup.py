#!/usr/bin/env python
#
# Copyright (C) 2020 Smithsonian Astrophysical Observatory
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

"""
python setup.py build -e '/usr/bin/env python' install --prefix=$ASCDS_INSTALL/contrib
"""


import os
from setuptools import setup
from setuptools.command.install import install

MYTOOL='acis_check_pha_range'

assert "ASCDS_INSTALL" in os.environ, "Please setup for CIAO before installing"

class InstallAhelpWrapper(install):
    'A simple wrapper to run ahelp -r after install to update ahelp index'

    @staticmethod
    def update_ahelp_database():
        'Run ahelp -r after install'
        print("Update ahelp database ...")
        from subprocess import check_output
        sout = check_output(["ahelp","-r"])
        for line in sout.decode().split("\n"):
            for summary in ["Processed", "Succeeded", "Failed", "Purged"]:
                if line.startswith(summary):
                    print("    "+line)
    
    def run(self):
        install.run(self)
        self.update_ahelp_database()



setup( name=MYTOOL,
       version='0.9.0',
       description='Compute approximate energy range used by acis',
       author='CXCSDS',
       author_email='glotfeltyk@si.edu',
       url='https://github.com/kglotfelty/'+MYTOOL,
       scripts=[MYTOOL,],
       data_files=[('param',[MYTOOL+'.par']),
                   ('share/doc/xml',[MYTOOL+'.xml']),
                  ],
       cmdclass={'install': InstallAhelpWrapper},
    )
