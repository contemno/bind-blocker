#!/usr/bin/python
import re, os, urllib2, requests

block_conffile = 'blocked.conf'

#blocklists array is in the format of [ [ URL, file format], ...]. File format is either: "hostlist" is list of domains or "hostfile" is a standard posix hostfile
blocklists = [
    ["https://pgl.yoyo.org/adservers/serverlist.php?hostformat=nohtml&mimetype=plaintext", "hostlist"],
    ["https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts", "hostsfile"],
    []
]

def is_valid_hostname(hostname):
    if 4 < len(hostname) < 256:
        #hostname = hostname[:-1] if hostname[-1] == "."
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))
    return False

def download_lists():
    fqdns = []
    for blocklist in blocklists:
        if len(blocklist) == 0:
            continue

        url, list_format  = blocklist

        res = urllib2.urlopen(url)
        res_text = res.read()
        if res.getcode() == 200 and len(res_text) < 1048576:
            lines = res_text.splitlines()
            if list_format == "hostsfile":
                for line in lines:
                    if "0.0.0.0" in line:
                        fqdns.append(line.split(' ')[1].lower())
            elif list_format == "hostlist":
                for line in lines:
                        fqdns.append(line.lower())
    print len(fqdns)
    return set(fqdns)

with open(block_conffile, 'w') as f:
  for fqdn in download_lists():
    if is_valid_hostname(fqdn):
      #f.write('zone "{0}" {{ type master; notify no; file "db.blocked"; }};\n'.format(fqdn))
      f.write('zone "{0}" {{ type master; notify no; file "db.blocked"; }};\n'.format(fqdn))
