#!"C:\Users\Senne Deproost\OneDrive - Vrije Universiteit Brussel\2017-2018\BP\Bachelorproef\MICO\WISDEM\OpenMDAO\openmdao-0.13.0\Scripts\python2.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'setuptools==38.5.1','console_scripts','easy_install-2.7'
__requires__ = 'setuptools==38.5.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('setuptools==38.5.1', 'console_scripts', 'easy_install-2.7')()
    )
