import threading 
import ctypes 
import time 

from threading import Thread
from backend import log_manager

"""
source: https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
Thread that runs the target in a while loop and can be killed at any time.
Works well for running led scripts
"""
class TerminationThread(threading.Thread): 
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None): 
        threading.Thread.__init__(self) 
        super().__init__(group=group, target=target, name=name, 
        args=args, kwargs=kwargs, daemon=daemon)

        #self._thread_id = thread_id
              
    def run(self): 
        # target function of the thread class 
        try: 
            if self._target:
                self._target(*self._args, **self._kwargs)
        except SystemExit:
            print('Exited thread {}'.format(self.name))
        finally: 
            print('ended') 
           
    def get_id(self):
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id
   
    def raise_exception(self): 
        thread_id = self.get_id() 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
              ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure')
            return False
        else:
            return True 

class ThreadingManager():
    def __init__(self, ignite_settings):
        #[thread id] = thread obj
        self.active_threads = dict()
        self.active_termination_threads = dict()
        self.thread_id_count = 0
        self.termination_id_count = 0
        pass
    
    def run_new_task(self, func, *args):
        id = self.thread_id_count
        proc = Thread(target=func, name=id, args=args)
        proc.start()
        self.active_threads[id] = proc
        self.thread_id_count += 1
        return id

    def run_new_termination_task(self, func, *args):
        id = self.termination_id_count
        term = TerminationThread(name=id, target=func, args=args)
        term.start()
        self.active_termination_threads[id] = term
        self.termination_id_count += 1
        return id

    def terminate_thread(self, id):
        if id not in self.active_termination_threads.keys():
            return
        term = self.active_termination_threads[id]
        for x in range(5):
            term.raise_exception()
            term.join(1.0)
            if not term.is_alive():
                self.active_termination_threads.pop(id)
                return True
        return False

    def terminate_all_termination_tasks(self, out_terminated_list=list()):
        terminated = list()
        for term in self.active_termination_threads:
            thread = self.active_termination_threads[term]
            for x in range(5):
                thread.raise_exception()
                thread.join(1.0)
                if not thread.is_alive():
                    terminated.append(term)
                    break
        
        for term in terminated:
            self.active_termination_threads.pop(term)
        
        out_terminated_list += terminated
                
        # self.__cleanup_termination_threads()

        if len(self.active_termination_threads) is not 0:
            return False
        else:
            return True

    def get_thread(self, id):
        return self.active_threads.get(id, None)
    
    def get_termination_thread(self, id):
        return self.active_termination_threads.get(id, None)

    def add_thread(thread:Thread):
        id = self.thread_id_count

        self.active_threads[id] = thread
        self.thread_id_count += 1
        return id
    
    def add_termination_thread(self, thread:TerminationThread, start_thread = False):
        id = self.termination_id_count
        self.active_termination_threads[id] = thread
        if start_thread and not thread.is_alive():
            thread.start()

        self.termination_id_count += 1
        return id

    def _cleanup_threads(self):
        for t in self.active_threads:
            thread = self.active_threads[t]
            if not thread.is_alive():
                self.active_threads.pop(t)
    
    def __cleanup_termination_threads(self):
        indices = list()
        for t in self.active_termination_threads:
            thread = self.active_termination_threads[t]
            if not thread.is_alive():
                indices.append(t)

        for index in indices:
            self.active_termination_threads.pop(index)

def _thread_end_callback(arg):
    pass

def _thread_error_callback(arg):
    pass





