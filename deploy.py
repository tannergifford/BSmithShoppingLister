import os
import zipfile
import shutil
import time

files = ('deliverables\\BeersmithShoppingLister.zip', 'dist\\', '__pycache__')

def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print('zipping %s as %s' % (os.path.join(dirname, filename), arcname))
            zf.write(absname, arcname)
    zf.close()

try:
    print('Cleaning directory')
    # Remove the files previously used for deployment
    for f in files:
        if os.path.exists(f):
            if os.path.isfile(f):
                os.remove(f)
            elif os.path.isdir(f):
                shutil.rmtree(f)
            else:
                print('Unable to determine ' + f)
            print('Removed ' + f)

    time.sleep(2)        

            
    print('Creating exe')
    # Create the executable and supporting files
    os.system("C:\\Python34\\python.exe setup.py py2exe")

    print('Zipping files')
    # Create the archive
    zip("dist", "deliverables\\BeerSmithShoppingLister")
    
    print('Done')
    
except:
    print('Unexpected error:', sys.exc_info()[1])
    raise
