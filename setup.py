from distutils.core import setup
import py2exe

Mydata_files = [('Images', ['Images\\icon.ico'])]

setup(
    name = "BeerSmith Shopping Lister",
    version = "0.1",
    description = "Creates a shopping list for a given BeerSmith recipe",
    author = "Tanner Gifford",
    windows=['BSmithShoppingLister.py'],
    data_files = Mydata_files
)
