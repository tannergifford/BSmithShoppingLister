from distutils.core import setup
import py2exe

Mydata_files = [('Images', ['Images\\icon.ico'])]

setup(
    name = "BeerSmith Shopping Lister",
    version = "0.1",
    description = "Creates a shopping list for a given BeerSmith recipe",
    author = "Tanner Gifford",
    windows=[{
        'script':'BSmithShoppingLister.py',
        'icon_resources': [(1, 'Images\\icon.ico')],
        'dest_base':'BSmithShoppingLister'
        }],
    data_files = Mydata_files,
    zipfile = None,
    options = {'py2exe': {'bundle_files': 2}}
)
