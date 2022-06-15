import winreg
import urllib.request
import zipfile
import json
import sys
import os
import subprocess

URL = 'https://registry.npmmirror.com/-/binary/chromedriver/'
DRIVER_PATH = r'..\drivers'

def getChromeVersion():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Google\Chrome\BLBeacon')
    chrome_version = winreg.QueryValueEx(key,'version')[0]
    return chrome_version

def getChromeDownloadURL(version='1.0'):
    _version = version[:version.rfind('.')]
    rep = urllib.request.urlopen(URL).read().decode('utf-8')
    result = json.loads(rep)
    versions = []
    for item in result:
        if item['type'] == 'file': continue
        if item['name'].find(_version)!=-1:
            versions.append(item)
    if len(versions)>0:
        return {
            'url':versions[-1]['url']+'chromedriver_win32.zip',
            'version':versions[-1]['name']
            }
    return None

def progressFunc(blocknum, blocksize, totalsize):
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    downsize = blocknum * blocksize

    if downsize >= totalsize:
        downsize = totalsize

    s = "%.2f%%" % (percent) + "====>" + "%.2f" % (downsize / 1024 / 1024) + "M/" + "%.2f" % (totalsize / 1024 / 1024) + "M \r"
    sys.stdout.write(s)
    sys.stdout.flush()
    if percent == 100:
        print('')
        
def downloadChromeDriver(url):
    folder = os.path.exists(DRIVER_PATH)
    if not folder:
        os.makedirs(DRIVER_PATH)
    filePath = os.path.join(DRIVER_PATH,'chromedriver.zip')
    urllib.request.urlretrieve(url,filePath,progressFunc)
    zFile = zipfile.ZipFile(filePath,'r')
    for file in zFile.namelist():
        zFile.extract(file,os.path.dirname(filePath))
    zFile.close()
    os.remove(filePath)

def getLocalChromeDriverVersion():
    folder = os.path.exists(DRIVER_PATH)
    if not folder:
        os.makedirs(DRIVER_PATH)
        return None
    cmd = r'{} --version'.format(os.path.join(DRIVER_PATH,'chromedriver.exe'))
    out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    out = out.decode('utf-8')
    _v = out.split(' ')[1]
    return _v

def update():
    chrome_v = getChromeVersion()
    local_v = getLocalChromeDriverVersion()
    last_v = getChromeDownloadURL(chrome_v)
    print(r'local version: {} last version: {}'.format(local_v,last_v['version']))
    if local_v == None or last_v['version']!=local_v:
        downloadChromeDriver(last_v['url'])