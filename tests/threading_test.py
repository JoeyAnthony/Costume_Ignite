import threading

from backend import threading_manager as th
#from backend.threading_manager import ThreadingManager, is_active, run_new_task
from backend import g_threading_manager as tm
import time
from backend import log_manager

def Test_All():
    log_manager.testlog("Testing threading")
    test_threading_manager()
    test_termination_thread()

    #test running and adding threads
    format_number = 0
    terminate_id = None
    for x in range(5):
        terminate_id = tm.run_new_termination_task(script_test_funct, ("thread {}".format(format_number),))
        format_number+=1

    assert(len(tm.active_termination_threads) == 5)
    assert(tm.terminate_thread(terminate_id))
    assert(len(tm.active_termination_threads) == 4)

    for x in range(5):
        thread = th.TerminationThread(name="script_thread_test {}".format(format_number), target=script_test_funct, args=("thread {}".format(format_number),))
        terminate_id = tm.add_termination_thread(thread, True)
        format_number+=1

    assert(len(tm.active_termination_threads) == 9)
    assert(tm.terminate_thread(terminate_id))
    assert(len(tm.active_termination_threads) == 8)
    assert(tm.terminate_all_termination_tasks())
    assert(len(tm.active_termination_threads)==0)

    log_manager.testlog("thread count is: {}".format(threading.active_count()))
    log_manager.testlog("threading_test passed all tests")

def test_termination_thread():
    #script thread test
    sthread = th.TerminationThread(name="script_thread_test", target=script_test_funct, args=("text1",))#must use , with strings to make a tuple
    log_manager.testlog("start script thread")
    sthread.start()
    assert sthread.is_alive()
    time.sleep(.5)
    sthread.raise_exception()
    sthread.join()
    assert not sthread.is_alive()
    log_manager.testlog("stop script thread")

def test_threading_manager():
        #threading manager
    id = tm.run_new_task(func, "test_thread" )
    proc = tm.get_thread(id)
    assert proc != None, "cannot get procces"

    proc.join(float(3.0))
    assert not proc.is_alive(), "Processs did not join"

def script_test_funct(give_text):
    while True:
        #print(give_text)
        x = give_text

def func(identifier):
    log_manager.testlog("starting thread %i", identifier)
    time.sleep(float(2.0))
    log_manager.testlog("stopping thread %i", identifier)

    
