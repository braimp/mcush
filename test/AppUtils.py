# coding: utf8
__doc__ = 'subprocess task control'
__author__ = 'Peng Shulin <trees_peng@163.com>'
from time import sleep
from Queue import Empty
from threading import Thread
from multiprocessing import Process, Queue
try:
    from termios import error as termios_error
except ImportError:
    termios_error = None
import Env
import Instrument

__INFO_STR = {
    'STOPPING': {'en': u'Stopping...',
                 'zh_cn': u'正在停止...',
                },
    'STOPPED':  {'en': u'Stopped',
                 'zh_cn': u'已停止',
                },
    'TIMEOUT':  {'en': u'Timeout',
                 'zh_cn': u'通讯超时',
                },
    'PORT_NOT_EXIST':   {'en': u'Communication port not exist',
                         'zh_cn': u'通讯端口不存在',
                        },
    'UNKNOWN_SERIAL_ERROR':     {'en': u'Unknown error',
                                'zh_cn': u'未知通讯错误',
                                },
    'UNKNOWN_ERROR':    {'en': u'Unknown error',
                         'zh_cn': u'未知错误',
                        },
}



def _getStr( key, lang=None ):
    if lang is None:
        lang = Env.LANGUAGE
    assert lang in Env.LANGUAGES
    return __INFO_STR[key][lang]


class Task():
    STOP_MAX_DELAY = 15
    STOP_CHECK_PERIOD = 0.2

    def __init__( self, args, queue ):
        self.args = args
        self.queue = queue
        self.control_queue = Queue()
        self.p = Process( target=self.monitor )
        self.p.start()
        self.listener = Thread( target=self.listener )
        self.listener.setDaemon( 1 )
        self.listener.start()
        self.manual_stop = False

    def target( self, args ):
        raise NotImplementedError

    def waitStop( self, timeout ):
        try:
            ret = self.control_queue.get( block=True, timeout=timeout  )
            assert ret == 'stop', ret
            self.info( _getStr('STOPPING') )
            return True
        except Empty:
            pass 
        return False

    def stop( self ):
        if not self.p.is_alive():
            return True
        self.manual_stop = True
        self.control_queue.put( 'stop' )
        for i in range( int(self.STOP_MAX_DELAY / self.STOP_CHECK_PERIOD) ):
            if not self.p.is_alive():
                return True
            else:
                sleep( self.STOP_CHECK_PERIOD )
        if Env.VERBOSE:
            print 'subprocess still alive'
        return False

    def info( self, info, info_type='info' ):
        self.queue.put( ('info', (info, info_type)) )

    def end( self ):
        self.queue.put( ('lock', False) )
        self.queue.put( ('end', False) )

    def monitor( self ):
        try:
            self.queue.put( ('lock', True) )
            self.target( self.args )
        except Instrument.CommandTimeoutError:
            self.info( _getStr('STOPPING') )
            self.info( _getStr('TIMEOUT'), 'error' )
        except Instrument.SerialNotFound, e:
            self.info( _getStr('PORT_NOT_EXIST') + ': ' + unicode(e), 'error' )
        except Instrument.UnknownSerialError, e:
            self.info( _getStr('UNKNOWN_SERIAL_ERROR') + ': ' + unicode(e), 'error' )
        except Exception, e:
            if Env.VERBOSE:
                print type(e), str(e)
            info = _getStr('UNKNOWN_ERROR') + ': '
            if termios_error and isinstance(e, termios_error):
                a,b = e.args
                info += u'%d %s'% (a, b.decode(encoding='utf8'))
            else:
                for c in str(e):  # e string may not be Unicode
                    info += c if ord(c) <= 128 else 'x%X'% ord(c)
            self.info( info, 'error' )
     
    def listener( self ):
        if self.p.is_alive():
            self.p.join()
        self.end()
       
    def isStopped( self ):
        return not self.p.is_alive()
 
    def terminate( self, safely=False ): 
        if safely:
            if self.stop():
                return
        if self.p.is_alive():
            self.p.terminate()
        self.info( _getStr('STOPPED') )
        self.end()

    def pause( self, prompt ):
        # clear queue
        while True:
            try:
                self.control_queue.get( block=False )
            except Empty:
                break
        self.queue.put( ('pause', prompt) )
        try:
            ret = self.control_queue.get( block=True, timeout=None )
            if ret == 'continue':
                return True 
        except Empty:
            pass
        return False

    def halt( self ):
        self.queue.put( ('halt', None) )
 
    def done( self ):
        self.queue.put( ('done', None) )


