# coding: utf8
__doc__ = 'basic environment'
__author__ = 'Peng Shulin <trees_peng@163.com>'
from os import getenv
from os.path import isdir, join
from sys import platform
from binascii import unhexlify
from tempfile import mktemp
from subprocess import check_output


_bool_true_list = ['1', 't', 'T', 'y', 'Y']
 
def getenv_bool( key, default=None ):
    ret = getenv(key, default)
    return False if ret is None else bool(ret in _bool_true_list)
 
def getenv_float( key, default=None ):
    ret = getenv(key, default)
    return None if ret is None else float(ret)
    
def getenv_int( key, default=None ):
    ret = getenv(key, default)
    try:
        if isinstance(ret, str):
            return int(eval(ret))
        else:
            return int(ret)
    except:
        return None
    #return None if ret is None else int(ret)

TEST_DIR = getenv('TEST_DIR')
if not TEST_DIR:
    if platform == 'linux2' and isdir( '/dev/shm' ):
        TEST_DIR = '/dev/shm'
    else:
        from tempfile import gettempdir
        TEST_DIR = gettempdir()

TEST_PREFIX = getenv('TEST_PREFIX', 'mcush_test' )
TEST_WR = mktemp( prefix=TEST_PREFIX + "_wr_", dir=TEST_DIR )
TEST_RD = mktemp( prefix=TEST_PREFIX + "_rd_", dir=TEST_DIR )

if platform == 'win32':
    PORT = getenv('PORT', 'COM1')
else:
    PORT = getenv('PORT', '/dev/ttyUSB0')
    PORTS = check_output(['allports']).strip()
    PORTS_LIST = PORTS.split(',')

BAUDRATE = getenv_int( 'BAUDRATE', 9600 )
RTSCTS = getenv_bool( 'RTSCTS' )
COMMAND_FAIL_RETRY = getenv_int( 'COMMAND_FAIL_RETRY', 3 )

DELAY = getenv_float( 'DELAY', 1 )
DELAY_AFTER_RESET = getenv_float( 'DELAY_AFTER_RESET', 1 )
RETRY = getenv_int( 'RETRY', 1000 )
NO_ECHO_CHECK = getenv_bool( 'NO_ECHO_CHECK' )
COMPACT_MODE = getenv_bool( 'COMPACT_MODE' )

DEVELOPMENT = getenv_bool( 'DEVELOPMENT' )
PROFILE = getenv_bool( 'PROFILE' )
LOGGING_FORMAT = getenv('LOGGING_FORMAT')

DEBUG = getenv_bool( 'DEBUG' )
VERBOSE = getenv_bool( 'VERBOSE' )
INFO = getenv_bool( 'INFO' )
WARNING = getenv_bool( 'WARNING' )


ESPEAK = getenv_bool( 'ESPEAK' )

PDF_READER = None
SOFFICE_BIN = None 
if platform == 'win32':
    PDF_READER = 'AcroRd32.exe'
    SOFFICE_BIN = 'soffice.exe'
    MPLAYER_BIN = 'mplayer.exe'
    NOTEPAD_BIN = 'notepad.exe'
elif platform == 'linux2':
    PDF_READER = '/usr/bin/evince'
    SOFFICE_BIN = '/usr/bin/soffice'
    MPLAYER_BIN = '/usr/bin/mplayer'
    NOTEPAD_BIN = '/usr/bin/mousepad'

REV = getenv_bool( 'REV' )

LANGUAGES = {'en', 'zh_cn'}
LANGUAGE = 'en'

try:
    from EnvExtra import *
except ImportError:
    pass


