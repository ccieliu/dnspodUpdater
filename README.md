# dnspodUpdater
* dnspod/tencent Cloud domain name commands tool.
* DNSPOD/腾讯云 域名解析 命令行工具
* Please update secretId && && domainName.
* 请更新secretId && secretKey && domainName
```python
class dnsAgent(object):
    def __init__(self):
        self.secretId = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        self.secretKey = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
        self.domainName = "aci.pub"
```
```bash
usage: acidns.py [-h] [-l] [-a [ADD [ADD ...]]] [-r REMOVE] [-e ENABLE]
                 [-d DISABLE]

optional arguments:
  -h, --help            show this help message and exit
  -l, --list, --show    List all ACI.PUB domains
  -a [ADD [ADD ...]], --add [ADD [ADD ...]]
                        Add a sub-domain to ACI.PUB,
                        Type: 'A', 'CNAME', 'MX', 'TXT', 'NS', 'AAAA', 'SRV'
                        Eg. 'acidns -a apic1 A 1.1.1.1'
  -r REMOVE, --remove REMOVE
                        Remove a sub-domain from ACI.PUB
                        Eg. 'acidns -r 549690747'
  -e ENABLE, --enable ENABLE
                        Enable a sub-domain in ACI.PUB
                        Eg. 'acidns -e 549690747'
  -d DISABLE, --disable DISABLE
                        Disable a sub-domain in ACI.PUB
                        Eg. 'acidns -d 549690747'
```
```bash
$ python acidns.py -l
+-----------+--------+-------+----------------+-----------------------+-------+---------------------+
|     ID    | STATUS |  TYPE |      NAME      |                 VALUE |  TTL  |        UPDATE       |
+-----------+--------+-------+----------------+-----------------------+-------+---------------------+
| 540245859 |   ON   |   NS  |       @        |   f1g1ns1.dnspod.net. | 86400 | 2020-02-04 16:54:23 |
| 540245860 |   ON   |   NS  |       @        |   f1g1ns2.dnspod.net. | 86400 | 2020-02-04 16:54:23 |
| 549239713 |   ON   |   NS  |       @        |           ad.aci.pub. |  600  | 2020-02-26 11:40:03 |
| 549225107 |   ON   |   A   |       ad       |          10.124.46.30 |  600  | 2020-02-26 10:38:20 |
| 545598340 |   ON   | CNAME |      docs      |    aci-pub.github.io. |  600  | 2020-02-17 10:42:37 |
| 549269837 |   ON   |   A   |      ise1      |          10.124.46.29 |  600  | 2020-02-26 12:35:46 |
| 549269259 |   ON   |  SRV  |    _gc._tcp    | 0 100 328 ad.aci.pub. |  600  | 2020-02-26 12:34:26 |
| 549269261 |   ON   |  SRV  | _kerberos._tcp |  0 100 88 ad.aci.pub. |  600  | 2020-02-26 12:34:26 |
| 549269269 |   ON   |  SRV  | _kerberos._udp |  0 100 88 ad.aci.pub. |  600  | 2020-02-26 12:34:26 |
| 549269263 |   ON   |  SRV  | _kpasswd._tcp  | 0 100 464 ad.aci.pub. |  600  | 2020-02-26 12:34:26 |
| 549269272 |   ON   |  SRV  | _kpasswd._udp  | 0 100 464 ad.aci.pub. |  600  | 2020-02-26 12:34:26 |
| 549269265 |   ON   |  SRV  |   _ldap._tcp   | 0 100 389 ad.aci.pub. |  600  | 2020-02-26 12:34:26 |
| 549246257 |   ON   |   NS  |     _msdcs     |           ad.aci.pub. |  600  | 2020-02-26 11:41:26 |
+-----------+--------+-------+----------------+-----------------------+-------+---------------------+
Records:  13
```