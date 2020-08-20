import time
import os
import multiprocessing as mp
from pymongo import MongoClient
folder = os.path.dirname(os.path.abspath(__file__))
folder = folder + '\logs'
#folder = os.path.abspath(__file__)
#folder = folder + '\logs'



def log_down():
    mongo = 'mongodb://' + os.environ['mongo_addr'] + ':27017/'
    client = MongoClient(mongo)
    mongo = client["logs"]
    index = 0
    lst_line = ''
    data=[]
    my_file = os.path.join(folder, 'down.log')
    while True:
        with open(my_file, 'rb') as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            lst=f.readline().decode()
            if lst_line.replace('\n','').replace('\r','')==lst.replace('\n','').replace('\r',''):
                print('no new update...')
                time.sleep(10)
                continue
        f.close()
        with open(my_file, 'r') as f1:

            for (i, line) in enumerate(f1):
                if (index >0  and i > index) or index ==0:
                    print(line)
                    obj = {}
                    obj['id'] = i
                    obj['log'] = line
                    data.append(obj)

            index,lst_line =i, line

            # dictToSend = {'status': os.environ.get('src_system')}
            # requests.post('http://' + str(os.environ.get('tracer_ip')) + ':' + str(5000) + '/soc', json=dictToSend)

        f.close()
        mongo["down"].insert_many(data)
        data=[]

def log_up():
    mongo = 'mongodb://' + os.environ['mongo_addr'] + ':27017/'
    client = MongoClient(mongo)
    mongo = client["logs"]
    index = 0
    lst_line = ''
    data=[]
    my_file = os.path.join(folder, 'up.log')
    while True:
        with open(my_file, 'rb') as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            lst=f.readline().decode()
            if lst_line.replace('\n','').replace('\r','')==lst.replace('\n','').replace('\r',''):
                print('no new update...')
                time.sleep(10)
                continue
        f.close()
        with open(my_file, 'r') as f1:

            for (i, line) in enumerate(f1):
                if (index >0  and i > index) or index ==0:
                    print(line)
                    #data.append('{' + line + '}')
                    obj = {}
                    obj['id'] = i
                    obj['log'] = line
                    data.append(obj)

            index,lst_line =i, line

            # dictToSend = {'status': os.environ.get('src_system')}
            # requests.post('http://' + str(os.environ.get('tracer_ip')) + ':' + str(5000) + '/soc', json=dictToSend)

        f.close()
        mongo['up'].insert_many(data)
        data = []

def log_gdc():
    mongo = 'mongodb://' + os.environ['mongo_addr'] + ':27017/'
    client = MongoClient(mongo)
    mongo = client["logs"]
    index = 0
    lst_line = ''
    data=[]
    my_file = os.path.join(folder, 'gcd.log')
    while True:
        with open(my_file, 'rb') as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            lst=f.readline().decode()
            if lst_line.replace('\n','').replace('\r','')==lst.replace('\n','').replace('\r',''):
                print('no new update...')
                time.sleep(10)
                continue
        f.close()
        with open(my_file, 'r') as f1:

            for (i, line) in enumerate(f1):
                if (index >0  and i > index) or index ==0:
                    print(line)
                    obj={}
                    obj['id']=i
                    obj['log']=line
                    data.append(obj)
            index,lst_line =i, line

            # dictToSend = {'status': os.environ.get('src_system')}
            # requests.post('http://' + str(os.environ.get('tracer_ip')) + ':' + str(5000) + '/soc', json=dictToSend)

        f.close()
        mongo['gcd'].insert_many(data)
        data=[]

if __name__ == '__main__':
    #os.environ['mongo_addr'] = '192.168.99.100'
    time.sleep(20)
    p1=mp.Process(target=log_up)
    p2 = mp.Process(target=log_down)
    p3 = mp.Process(target=log_gdc)
    p1.start()
    p2.start()
    p3.start()