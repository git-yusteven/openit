import time
import subprocess
import atexit
from multiprocessing import Process, Manager, Semaphore
from clash import push, checkenv
from check import check
from tqdm import tqdm
from init import init, clean

if __name__ == '__main__':
    with Manager() as manager:
        alive = manager.list()
        http_port, api_port, threads, source, timeout, outfile, proxyconfig, apiurl, testurl, config= init()
        clashname, operating_system = checkenv()
        print('Clash is Running on '+ operating_system)
        clash = subprocess.Popen([clashname, '-f', './temp/working.yaml', '-d', '.'])
        processes =[]
        sema = Semaphore(threads)
        time.sleep(5)
        for i in tqdm(range(int(len(config['proxies']))), desc="Testing"):
            sema.acquire()
            p = Process(target=check, args=(alive,config['proxies'][i],apiurl,sema,timeout,testurl))
            try:
                p.start()
                processes.append(p)
            except:
                continue
        for p in processes:
            p.join
        time.sleep(5)
        alive=list(alive)
        push(alive,outfile)
        atexit.register(clean, clash)
