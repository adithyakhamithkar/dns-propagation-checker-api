#!/usr/bin/env python
# Objective to get a list of DNS records from different name servers
# Dependancies dnspython==1.16.0
import socket
import dns.resolver
import logging
import json


logger = logging.getLogger()


def GetPropagationList(FQDN, DNS_RECORD):
    # Variables
    NSList = []
    PropagationList = []
    IPList = []
    List = ['Primary', 'Secondary']

    # Get list of DNS_Providers
    with open('api/resources/dns-list.json') as f:
        DNSList = json.load(f)
    f.close()
    json_lenght = len(DNSList)
    for i in range(0, json_lenght):
        for l in List:
            NS = DNSList[i][l]
            try:
                logger.debug("Trying to resolve DNS from " +
                             DNSList[i]['DNS_Provider'] + ' : ' + NS)
                myResolver = dns.resolver.Resolver()
                myResolver.nameservers = [socket.gethostbyname(NS)]
                myResolver.lifetime = myResolver.timeout = 5.0
                myAnswers = myResolver.query(FQDN, DNS_RECORD)
                for answer in myAnswers:
                    logger.debug(str(answer.to_text()))
                    IPList.append(str(answer.to_text()))
                PropagationList.append(
                    {'DNS_Provider': DNSList[i]['DNS_Provider'], str(NS): str(IPList)})
                del IPList[:]
            except (dns.resolver.NXDOMAIN):
                logger.exception(dns.resolver.NXDOMAIN)
                PropagationList.append(
                    {'DNS_Provider': DNSList[i]['DNS_Provider'], str(NS): "Could not resolve DNS"})
            except (dns.resolver.NoAnswer):
                logger.exception(dns.resolver.NoAnswer)
                PropagationList.append(
                    {'DNS_Provider': DNSList[i]['DNS_Provider'], str(NS): "No Answer from DNS"})
            except (dns.exception.Timeout):
                logger.exception(dns.exception.Timeout)
                PropagationList.append(
                    {'DNS_Provider': DNSList[i]['DNS_Provider'], str(NS): "Connection time from DNS"})
            except:
                message = "Please check the FQDN or the DNS record type"
                logger.exception(message)
                PropagationList.append(
                    {'DNS_Provider': DNSList[i]['DNS_Provider'], str(NS): message})

    logger.debug(str(PropagationList))
    HostInfo = {'DNS_Query': {'Host': str(FQDN), 'DNS_Record': str(
        DNS_RECORD)}, "Result": {'DNS_Propagation': PropagationList}}
    return HostInfo
