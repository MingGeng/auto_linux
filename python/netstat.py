#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob

PROC_FILE = {
        'tcp' : '/proc/net/tcp',
        'tcp6' : '/proc/net/tcp6',
        'udp' : '/proc/net/udp',
        'udp6' : '/proc/net/udp6'
        }
STATUS = {
        '01': 'ESTABLISHED',
        '02': 'SYN_SENT',
        '03': 'SYN_RECV',
        '04': 'FIN_WAIT1',
        '05': 'FIN_WAIT2',
        '06': 'TIME_WAIT',
        '07': 'CLOSE_WAIT',
        '08': 'CLOSE_ACK',
        '09': 'LAST_ACK',
        '0A': 'LISTEN',
        '0B': 'CLOSING',
        }

def get_program_name(pid):
    '''get program name
    '''
    path = '/proc/' + str(pid) + '/comm'

    with open(path, 'r') as file:
        content = file.read()
    content = content.strip()
    return content

def convert_ip_port(ip_port):
    '''convert ip port
    '''
    ip, port = ip_port.split(":")
    port = int(port, 16)
    ip = [str(int(ip[6:8], 16)), str(int(ip[4:6], 16)), str(int(ip[2:4],16)), str(int(ip[0:2],16))]
    ip = '.'.join(ip)
    return ip, port




def get_content(type):
    '''get proc file content
    '''
    with open(PROC_FILE[type], 'r') as file:
        content = file.readlines()
        content.pop(0)
    return content
        
def main(choose):
    '''get and show port info 
    '''
    templ = "%-5s %-30s %-30s %-13s %-6s %s"
    print(templ % ("Proto", "Local address", "Remote address", "Status", "PID", "Program name"))
    content = get_content(choose)

    for info in content:
        items = info.split()
        proto = choose
        local_addr = "%s:%s" % convert_ip_port(items[1])
        status = STATUS[items[3]]
        if status == 'LISTEN':
            remote_addr = '-'
        else:
            remote_addr = "%s:%s" % convert_ip_port(items[2])
        pid = get_pid(items[9])
        program_name = ''
        if pid:
            program_name = get_program_name(pid)
        
        print(templ % (
            proto,
            local_addr,
            remote_addr,
            status,
            pid or '-',
            program_name or '-'
            ))

        


def get_pid(inode):
    for path in glob.glob('/proc/[0-9]*/fd/[0-9]*'):
        try:
            if str(inode) in os.readlink(path):
                return path.split('/')[2]
            else:
                continue
        except:
            pass
    return None


if __name__ == '__main__':
    choose = 'tcp'
    if len(sys.argv) > 1:
        choose = sys.argv[1]
    main(choose)


