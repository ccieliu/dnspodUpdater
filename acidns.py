import argparse
import requests
import hmac
import hashlib
import base64
import time
import random
import urllib.parse
import pprint
import json
from prettytable import PrettyTable

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-l", "--list", "--show",
                    action="store_true", help="List all ACI.PUB domains")
parser.add_argument("-a", "--add", nargs="*",
                    help="""Add a sub-domain to ACI.PUB, 
Type: 'A', 'CNAME', 'MX', 'TXT', 'NS', 'AAAA', 'SRV'
Eg. 'acidns -a apic1 A 1.1.1.1' """)
parser.add_argument("-r", "--remove", help="""Remove a sub-domain from ACI.PUB
Eg. 'acidns -r 549690747' """)
parser.add_argument("-e", "--enable", help="""Enable a sub-domain in ACI.PUB
Eg. 'acidns -e 549690747' """)

parser.add_argument("-d", "--disable", help="""Disable a sub-domain in ACI.PUB
Eg. 'acidns -d 549690747' """)
parser.add_argument("-m", "--modify", nargs="*",
                    help="""Modify a sub-domain in ACI.PUB
Eg. 'acidns -m 549690747 test A 2.2.2.2' """)

args = parser.parse_args()


class dnsAgent(object):
    def __init__(self):
        self.secretId = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        self.secretKey = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
        self.domainName = "aci.pub"
        self.dnsUrl = "cns.api.qcloud.com/v2/index.php"
        self.Timestamp = str(int(time.time()))
        self.Nonce = str(random.randint(00000, 99999))

    def getSig(self, method, originalDic):
        originalKeyList = []
        sortedStr = ""
        originalDic["Timestamp"] = self.Timestamp
        originalDic["Nonce"] = self.Nonce
        originalDic["SecretId"] = self.secretId
        for i in originalDic:
            originalKeyList.append(i)
        sortedList = sorted(originalKeyList)
        for i in sortedList:
            sortedStr += i+"="+str(originalDic[i])+"&"
        sortedStr = sortedStr.rstrip("&")
        hashStr = method+self.dnsUrl+"?"+sortedStr
        message = bytes(hashStr, 'utf-8')
        secret = bytes(self.secretKey, 'utf-8')
        signature = base64.b64encode(
            hmac.new(secret, message, digestmod=hashlib.sha1).digest())
        # print(message)
        return(urllib.parse.quote(signature.decode('utf-8'), safe=''))

    def listDns(self):
        originalDic = {"Action": "RecordList",
                       "length": "100",
                       "domain": self.domainName,
                       "Timestamp": self.Timestamp,
                       "Nonce": self.Nonce}
        rJson = self.takeAction(originalDic=originalDic)

        recoardsJson = rJson["data"]["records"]
        infoJson = rJson["data"]["info"]
        t = PrettyTable(['ID', 'STATUS', 'TYPE', 'NAME',
                         'VALUE', 'TTL', 'UPDATE'])
        t.align["VALUE"] = "r"
        for i in recoardsJson:
            if i["enabled"] == 1:
                status = "ON"
            else:
                status = "OFF"
            t.add_row([i["id"], status, i["type"],
                       i["name"], i["value"], i['ttl'], i["updated_on"]])
        print(t)

        print("Records: ", infoJson["records_num"])

    def takeAction(self, originalDic):
        signature = self.getSig(method="GET", originalDic=originalDic)
        originalDic["Signature"] = signature
        tmpUrl = ""
        for i in originalDic:
            tmpUrl += i+"="+str(originalDic[i])+"&"
        tmpUrl = tmpUrl.rstrip("&")
        getURL = "https://" + self.dnsUrl + "?"+tmpUrl
        s = requests.session()
        r = s.get(url=getURL)
        rJson = r.json()
        # print(getURL)
        return(rJson)

    def modDns(self, recordId, subDomain, recordType, value):
        originalDic = {"Action": "RecordModify",
                       "subDomain": subDomain,
                       "recordId": recordId,
                       "domain": self.domainName,
                       "recordType": recordType,
                       "recordLine": "默认",
                       "value": value,
                       "Timestamp": self.Timestamp,
                       "Nonce": self.Nonce}
        rJson = self.takeAction(originalDic=originalDic)
        if rJson["code"] == 0:
            print(rJson["codeDesc"])
        else:
            print(rJson["codeDesc"]+": " + rJson["message"])

    def addDns(self, subDomain, recordType, value):
        if recordType.upper() in ["A", "CNAME", "MX", "TXT", "NS", "AAAA", "SRV"]:
            originalDic = {"Action": "RecordCreate",
                           "subDomain": subDomain,
                           "domain": self.domainName,
                           "recordType": recordType,
                           "recordLine": "默认",
                           "value": value,
                           "Timestamp": self.Timestamp,
                           "Nonce": self.Nonce}
            rJson = self.takeAction(originalDic=originalDic)
            if rJson["code"] == 0:
                print(rJson["codeDesc"])
            else:
                print(rJson["codeDesc"]+": " + rJson["message"])
        else:
            print("Type should in 'A', 'CNAME', 'MX', 'TXT', 'NS', 'AAAA', 'SRV' ")

    def removeDns(self, recordId):
        originalDic = {"Action": "RecordDelete",
                       "recordId": recordId,
                       "domain": self.domainName,
                       "Timestamp": self.Timestamp,
                       "Nonce": self.Nonce}
        rJson = self.takeAction(originalDic=originalDic)
        if rJson["code"] == 0:
            print(rJson["codeDesc"])
        else:
            print(rJson["codeDesc"]+": " + rJson["message"])

    def enableDns(self, recordId):
        originalDic = {"Action": "RecordStatus",
                       "recordId": recordId,
                       "status": "enable",
                       "domain": self.domainName,
                       "Timestamp": self.Timestamp,
                       "Nonce": self.Nonce}
        rJson = self.takeAction(originalDic=originalDic)
        if rJson["code"] == 0:
            print(rJson["codeDesc"])
        else:
            print(rJson["codeDesc"]+": " + rJson["message"])

    def disableDns(self, recordId):
        originalDic = {"Action": "RecordStatus",
                       "recordId": recordId,
                       "status": "disable",
                       "domain": self.domainName,
                       "Timestamp": self.Timestamp,
                       "Nonce": self.Nonce}
        rJson = self.takeAction(originalDic=originalDic)
        if rJson["code"] == 0:
            print(rJson["codeDesc"])
        else:
            print(rJson["codeDesc"]+": " + rJson["message"])


if __name__ == "__main__":
    # print(args)
    myobj = dnsAgent()
    if args.list == True:
        myobj.listDns()
    elif args.add != None:
        subDomain = args.add[0]
        recordType = args.add[1]
        value = args.add[2]
        myobj.addDns(subDomain=subDomain, recordType=recordType, value=value)
    elif args.remove != None:
        recordId = args.remove
        myobj.removeDns(recordId=recordId)
    elif args.modify != None:
        recordId = args.modify[0]
        subDomain = args.modify[1]
        recordType = args.modify[2]
        value = args.modify[3]
        myobj.modDns(recordId=recordId,subDomain=subDomain, recordType=recordType, value=value)
    elif args.enable != None:
        recordId = args.enable
        myobj.enableDns(recordId=recordId)
    elif args.disable != None:
        recordId = args.disable
        myobj.disableDns(recordId=recordId)
    else:
        parser.print_help()
