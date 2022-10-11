import os
import sys
import django
base = os.getcwd()
new = os.path.join(base,'SmartReceptionist\server')
#os.chdir(new)
sys.path.append(new)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','server.settings')
def start():

    print('done setup')