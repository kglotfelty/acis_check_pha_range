

import os

assert "ASCDS_INSTALL" in os.environ, "Please setup for CIAO before installing"


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
