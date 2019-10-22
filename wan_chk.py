#!/usr/local/bin/python2
import os
import subprocess
import shlex
command_line = "ping -c 1 -S 123.201.63.143  123.201.63.129"
args = shlex.split(command_line)

try:
    subprocess.check_call(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if os.stat('/usr/local/etc/squid/advance.conf').st_size > 10:
        print ("We are on PRI WAN")
    else:
        print ("making changes in squid file")
        os.system('echo acl lan_src src 192.168.1.0/24 > /usr/local/etc/squid/advance.conf && echo tcp_outgoing_address 123.201.63.143 lan_src >> /usr/local/etc/squid/advance.conf')
        os.system('/usr/local/sbin/squid -k reconfigure')
except subprocess.CalledProcessError:
    if os.stat('/usr/local/etc/squid/advance.conf').st_size < 10:
        print ("we are on BKP wan, waitng for PRI WAN")
    else:
        os.system('echo > /usr/local/etc/squid/advance.conf')
        os.system('/usr/local/sbin/squid -k reconfigure')

