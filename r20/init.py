from configparser import ConfigParser
from pathlib import Path
import os
import sys
import shutil
from subprocess import run

COLON=':'

CPX=ConfigParser()
CPH=ConfigParser()

assert os.environ.get('RXX')
RXXX = Path( os.environ['RXX'] )
HOME= Path( os.environ['HOME'] )

HOME_CFG=ConfigParser()
RXXX_CFG=ConfigParser()
HOME_CFG.read(HOME/'.config/r20/config.ini')
RXXX_CFG.read(RXXX/'config/config.ini')

CACHE=None
try: CACHE=HOME/Path( HOME_CFG['global']['cache'] ) 
except KeyError: pass
try: CACHE=RXXX/Path( RXXX_CFG['global']['cache'] ) 
except KeyError: pass
assert CACHE



def log(*args): sys.stderr.write( 'WITH: %s \n' % str(args) )
def fix(pth): 
    aa=pth.split('/')
    bb=list(filter(None,aa))
    # We want to change 'https:' to 'http'
    while bb[0].endswith(':'):
        bb[0]=bb[0][:-1]
    return '/'.join(bb)

def cached4remote(remote):
    remote = str(remote)
    url, inner = remote.split()
    dst = DOWNLOAD/fix(url)
    if not dst.is_dir():
        run( ['git', 'clone', url, dst] )
    return dst/inner

def main():
    DD=dict()
    for name, remote in CONFIG['external'].items():
        cached = str(cached4remote(remote))
        DD[name] = cached
        sys.path.append(cached)
    for name, local in CONFIG['internal'].items():
        log( 5555, local)
        DD[name]=str(RXXX/local)
        log(5556,  DD[name])
    oldparts = os.environ.get('PYTHONPATH','').split(':')
    newparts = list(DD.values())
    allparts = newparts + oldparts
    os.environ['PYTHONPATH'] = COLON.join( allparts )

if __name__=="__main__":
    DOWNLOAD=CACHE
    CONFIG=RXXX_CFG
    main()
    print( os.environ['PYTHONPATH'] )
    #run( ARGS )
