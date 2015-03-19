#!/usr/bin/env python
"""
This script copies my personal BibTeX file to the current directory.
"""

import os
import shutil
import sys
if sys.version_info[0] == 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve
    FileNotFoundError = IOError

bibpath = os.path.join(os.path.expanduser("~"), "Google Drive",
                       "Library", "Library.bib")
biburl = "https://raw.githubusercontent.com/petebachant/Library/master/Library.bib"
                       
try:
    shutil.copy2(bibpath, "library.bib")
except FileNotFoundError:
    print("Downloading BibTeX file")
    urlretrieve(biburl, "library.bib")