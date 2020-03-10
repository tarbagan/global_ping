# -*- coding: utf-8 -*-
import speedtest
import subprocess
import platform
from multiprocessing.dummy import Pool as ThreadPool
import csv

def server():
    '''Get the speedtest.net servers (7k servers)'''
    ser_all = []
    s = speedtest.Speedtest()
    for i in s.get_servers().values():
        for srv in i:
            srv['host'] = srv['host'][:-5]
            ser_all.append(srv)
    return ser_all

def ping(host):
    '''The ping function for windows os ping'''
    try:
        ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"
        args = "ping " + " " + ping_str + " " + host
        con_out = subprocess.check_output(args, shell=True).decode('cp866')
        con_out = (con_out.split( '=' )[2])[:-6]
    except:
        con_out = 0
    return con_out

def split(arr, count):
    '''We break lists -server()- by an amount of flows of Pool'''
    return [arr[i::count] for i in range(count)]

pool = ThreadPool(5)

for part in (split(server(), 1700)):
    try:
        hosts_part = [i['host'] for i in part]
        ttl_all = pool.map(ping, hosts_part)
        cnt = len(ttl_all)
    except:
        z=0

    '''save result to csv file'''
    with open( 'ping.csv', 'a') as f:
        for num, i in enumerate(part):
            i['ttl'] = ttl_all[num]

            lat=str(i['lat'])
            lon=str(i['lon'])
            name=str(i['name'])
            country=str(i['country'])
            id=str(i['id'])
            hostst=str(i['host'])
            ttlst=str(i['ttl'])
            d=str(i['d'])
            stroka = id + ';' + name + ';' + country + ';' + lat + ';' + lon + ';' + hostst + ';' + d + ';' + ttlst
            print (stroka)

            try:
                f.write(str(stroka) +'\n')
            except:
                z=0
        f.close()
print ('ok')
