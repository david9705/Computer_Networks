# -*- coding: UTF-8 -*-
import dpkt
import socket
import datetime
import matplotlib.pyplot as plt

first = 0
first_ts = 0
first_seq = 0
first1 = 0
first_ts1 = 0
first_seq1= 0
def printPcap(pcap):
    global first
    global first_ts
    global first_seq
    global first1
    global first_ts1
    global first_seq1
    list_ts = []
    list_ts1 = []
    list_sqn = []
    list_sqn1 = []

    for (ts,buf) in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        if not isinstance(eth.data, dpkt.ip.IP):
            print 'Non IP Packet type not supported %s' % eth.data.__class__.__name__
            continue

        ip = eth.data
        src = socket.inet_ntoa(ip.src)
        dst = socket.inet_ntoa(ip.dst)

        tcp = ip.data

        if src == "140.113.195.91" and tcp.dport == 56018:
            if first == 0:
                first = 1
                first_ts = ts
                first_seq = tcp.seq
                old_ts=0
                buf_sum=0
            buf_sum=buf_sum+len(buf)
            if (ts - old_ts) >= 0.1:
                old_ts=ts
		list_ts.append(ts-first_ts)
                list_sqn.append (buf_sum*10)
                buf_sum=0

        if src == "140.113.195.91" and tcp.dport == 56020:
            if first1 == 0:
                first1 = 1
                first_ts1 = ts
                first_seq1 = tcp.seq
                old_ts1=0
                buf_sum1=0
            buf_sum1=buf_sum1+len(buf)
            if (ts - old_ts1) >= 0.1:
                old_ts1=ts
		list_ts1.append(ts-first_ts1)
                list_sqn1.append (buf_sum1*10)
                buf_sum1=0

           

            
    draw_sqn(list_ts,list_sqn,list_ts1,list_sqn1)

def draw_sqn(list_ts,list_sqn,list_ts1,list_sqn1):

    plt.plot(list_ts,list_sqn)
    plt.plot(list_ts1,list_sqn1)
    plt.xlabel("Time");
    plt.ylabel("Throughput");
    plt.title("time/sequence graph")
    plt.show()

def main():
    f = open('lab1_0413354_rx_wget.pcap')
    pcap = dpkt.pcap.Reader(f)
    printPcap(pcap)

if __name__ == '__main__':
    main()

