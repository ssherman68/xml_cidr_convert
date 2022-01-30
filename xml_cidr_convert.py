#! /usr/bin/env python

'''
MS XML CIDR -> subnet converter

First Version: 2/21/18 Stacy Sherman

-Takes an XML formatted list of CIDR IPv4 IP networks from Microsoft
-Converts them to subnet mask format
-Outputs them as a Cisco friendly IP object group

Input XML file looks like:

<product name="EOP">
  <addresslist type="IPv4">
    <address>23.103.132.0/22</address>
    <address>23.103.136.0/21</address>
  </addresslist>
</product>

Output looks like:

object-group network ms_eop
 network-object 23.103.132.0 255.255.252.0
 network-object 23.103.136.0 255.255.248.0

The object group can then be copied/pasted into a firewall or other cisco
device. It could also serve as an input to a Cisco API to directly modify
the group.

Libraries required:

ElementTree
ipaddress

'''
# Import any modules

import xml.etree.ElementTree as ET
import re
import ipaddress
from pprint import pprint

def get_ip_xml(input_file):

    # Parses a specifically formatted XML file (see above) and returns a list
    # of IP networks from the file. Currently it assumes anything with the
    # address tag is needed. Later this will be expanded to pull
    # certain types of product IPs and handle more situations.

    ip_list = []
    tree = ET.parse(input_file)                  # Read input file into element tree
    for elem in tree.iter(tag='address'):        # Get anything with the 'address' tag
       ip_list.append(elem.text)                 # add it to the list
    return ip_list


def cidr2subnet(cidr_net):

    # Takes a string with a CIDR network (i.e. '192.168.1.0/24') and converts
    # it to subnet mask notation: 192.168.1.0 255.255.255.0. Returns the
    # network and the netmask. Requires the ipaddress & re (regex) libraries

    n = re.search('(.*)/',cidr_net)
    network = n.group(1)
    cidr_net = unicode(cidr_net, "utf-8")
    net4 = ipaddress.ip_network(cidr_net)
    netmask = str(net4.netmask)
    return network, netmask

def cidr2asagroup (ip_list):

    # Takes a list of CIDR formatted networks and converts them
    # to a Cisco ASA subnet style network group with the format:
    # object-group network my_group
    #  network object 192.168.1.0 255.255.255.0
    #  network object 172.16.0.0 255.255.0.0

    print "Converting to a Cisco network object group\n"
    gname = raw_input ("Enter the network object group name ===> ")
    if gname == '':
        gname = '<NAMEHERE>'
    obj_group = 'object-group network ' + gname + '\n'
    for cidr in ip_list:
        network, netmask = cidr2subnet(cidr)
        obj_group += ' network-object %s %s \n' % (network, netmask)
    print "\nHere is your object group:\n\n"
    print obj_group
    return obj_group


def main():
    print "Enter the name of the XML formatted file\n"
    input_file = raw_input("===> ")
    ip_list = get_ip_xml(input_file)
    obj_group = cidr2asagroup(ip_list)


if __name__ == '__main__':
    main()

