

import os
import sys

assert "ASCDS_INSTALL" in os.environ, "Please setup for CIAO before installing"

# Set PYVER env variable so that it'll get replaced in setup.cfg
ver = sys.version_info
os.environ["PYVER"] = "python{}.{}".format(ver[0],ver[1]) 


from distutils.core import setup

setup( name='acis_check_pha_range',
       version='0.1.0',
       description='Compute approximate energy range used by acis',
       author='Anonymous',
       author_email='glotfeltyk@si.edu',
       url='https://github.com/kglotfelty/acis_check_pha_range/',
       scripts=["acis_check_pha_range"],
       data_files=[('param',['acis_check_pha_range.par']),
                    ]
                    
    )
