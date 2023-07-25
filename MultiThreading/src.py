from cloud_connect import CloudConnection
from threading import Thread, Lock
import logging
import time

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s (T:%(thread)d):- %(message)s")



class InCom(Thread):
    # do InCom
    b = 2
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._lock = kwargs.get("lock", None)

class QtUI(Thread):
    # do UI
    c = 3
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._lock = kwargs.get("lock", None)

def main():
    ExternalComm_thr = CloudConnection()
    InternalComm_thr = InCom()
    QtUI_Update_thr = QtUI()
    
    ExternalComm_thr.start()
    InternalComm_thr.start()
    QtUI_Update_thr.start()
    
    ExternalComm_thr.join()
    InternalComm_thr.join()
    QtUI_Update_thr.join()
    
    
if __name__ == "__main__":
    main()