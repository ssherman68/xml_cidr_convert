README.md

NOTE: O365 XML files were phased out in October 2018:

https://docs.microsoft.com/en-us/microsoft-365/enterprise/microsoft-365-ip-web-service?view=o365-worldwide


MS XML CIDR -> subnet converter

First Version: 2/21/18 Stacy Sherman

-Takes an XML formatted list of CIDR IPv4 IP networks from Microsoft
-Converts them to subnet mask format
-Outputs them as a Cisco friendly IP object group

The XML file must be downloaded and available.

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

elementtree
ipaddress
re (regex)
