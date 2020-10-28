#!/usr/bin/env python
# Objective to get a whois records
# Dependancies python-whois

import whois

def GetWhois(FQDN):
    w = whois.whois(FQDN)
    return w
