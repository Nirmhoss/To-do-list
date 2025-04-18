# docs/conf.py
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
]

html_theme = 'sphinx_rtd_theme'

autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

# Виключення деяких попереджень
suppress_warnings = ['app.add_node']