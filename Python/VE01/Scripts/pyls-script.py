#!c:\sandbox\python\ve01\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'python-language-server==0.18.0','console_scripts','pyls'
__requires__ = 'python-language-server==0.18.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('python-language-server==0.18.0', 'console_scripts', 'pyls')()
    )
