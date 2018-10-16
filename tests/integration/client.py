#!/usr/bin/python

import ast
import json
import requests
import subprocess

from requests.exceptions import ConnectionError

baseurl = "http://localhost:5000"

url_hub = [baseurl + "/inbound/sms/",
           baseurl + "/inbound/",
           baseurl + "/outbound/sms/"]


creds = ("azr1", "20S0KPNOIM")

def sendRequest(url, data, auth=""):
    """Sends request to  the server."""
    try:
        resp = requests.post(url=url, data=json.dumps(data),
                             auth=auth, timeout=60)

        if resp.status_code == 405:
            print ast.literal_eval(resp.text)

        elif resp.status_code == 200:
            print ast.literal_eval(resp.text)
        elif resp.status_code == 403:
            print ast.literal_eval(resp.text)
        else:
            print resp.status_code
            

    except ConnectionError:
        print "Server is down"

"""
data_dict = [{"from": "998085790", "to": "850018531", "text": "How are you ?"},
             {"from": "", "to": "850018531", "text": "How are you ?"},
             {"from": "998085790", "to": "", "text": "How are you ?"},
             {"from": "9980857905", "to": "4924195509192", "text": ""},
             {"from": "4924195509049", "to": "4924195509192",
              "text": "How are you ?"},
             {"from": "4924195509049", "to": "4924195509192",
              "text": "Lets STOP the chat."}

            ]
"""

#------------
# TEST CASES:
#------------

# CASE: Invalid numbers
print "----------------------- Invalid numbers  -------------------------"
data = {"from": "998085790", "to": "850018531", "text": "How are you ?"}
sendRequest(url_hub[0], data,  auth=creds)


# CASE: from param missing

print "\n\n"
print "-----------------------  from param missing   -------------------------"
data = {"from": "", "to": "850018531", "text": "How are you ?"}
sendRequest(url_hub[0], data,  auth=creds)
sendRequest(url_hub[2], data,  auth=creds)

# CASE: to param missing

print "\n\n"
print "-----------------------  to param missing   -------------------------"
data = {"from": "998085790", "to": "", "text": "How are you ?"}
sendRequest(url_hub[0], data,  auth=creds)
sendRequest(url_hub[2], data,  auth=creds)

# CASE: text param missing

print "\n\n"
print "-----------------------  text param missing  -------------------------"
data = {"from": "9980857905", "to": "4924195509192", "text": ""}
sendRequest(url_hub[0], data,  auth=creds)
sendRequest(url_hub[2], data,  auth=creds)


print "\n\n"
print "-----------------------  from is invalid   -------------------------"
data = {"from": "324324322", "to": "4924195509192", "text": "How are you ?"}
sendRequest(url_hub[0], data,  auth=creds)

# CASE: to param missing

print "\n\n"
print "-----------------------  to is invalid   -------------------------"
data = {"from": "4924195509049", "to": "32432432", "text": "How are you ?"}
sendRequest(url_hub[0], data,  auth=creds)

# CASE: text param missing

print "\n\n"
print "-----------------------  text is invalid  -------------------------"
invalid_text = "dsdwqiuoirrrrrrrrrrrrrmwrcuewroiwmfcwuifxnueioe uueoi uOIRERU\
IDEWIUNUIEWNURCIWNUEIFNUWIUFmneFRYBEWCNe8ruffircniunywarewrcIREIURNYMRNYUINYC\
MUOIEWWWWWWR UEWAOIRUEUFOIEAUROIEWUOIUEWAROIUEWAOIMAOIRUAOIXEMCWRUMROIEUIRMR"
data = {"from": "9980857905", "to": "4924195509192", "text": invalid_text}
sendRequest(url_hub[0], data,  auth=creds)

# CASE: inbound sms ok

print "\n\n"
print "-----------------------  inbound sms ok   -------------------------"
data = {"from": "4924195509049", "to": "4924195509192", "text": "Hi"}
sendRequest(url_hub[0], data,  auth=creds)

# CASE:  outbound sms ok

print "\n\n"
print "-----------------------  outbound sms ok   -------------------------"
data = {"from": "4924195509192", "to": "4924195509049", "text": "Hello"}
sendRequest(url_hub[2], data,  auth=creds)

# CASE: STOP the chat

print "\n\n"
print "-----------------------  STOP the chat   -------------------------"
data = {"from": "4924195509049", "to": "4924195509192",
        "text": "Lets STOP the chat."}
sendRequest(url_hub[0], data,  auth=creds)

# CASE: blocked by STOP request

print "\n\n"
print "----------------------- blocked by STOP request   -------------------------"
# data = {"from": "4924195509049", "to": "4924195509192", "text": " Hey there!, STOP"}
data = {"from": "4924195509049", "to": "4924195509192", "text": " Hey there!"}
sendRequest(url_hub[2], data,  auth=creds)

# CASE: authentication failed(403)

print "\n\n"
print "-----------------------  authentication failed(403)   -------------------------"
data = {"from": "4924195509049", "to": "4924195509192", "text": " Hey there!"}
err_creds = ("azr1", "20S0KPNOIO")
sendRequest(url_hub[2], data,  auth=err_creds)
  

# CASE: 405
print "\n\n"
print "----------------------- Non POST method  (405)   -------------------------"
data = {"from": "4924195509049", "to": "4924195509192", "text": " Hey there!"}
err_creds = ("azr1", "20S0KPNOIO")
resp = requests.get(url=url_hub[2], data=json.dumps(data), auth=creds, timeout=60)
print resp.status_code

# CASE: 404

print "\n\n"
print "-----------------------  404   -------------------------"
data = {"from": "4924195509049", "to": "4924195509192", "text": " Hey there!"}
sendRequest(url_hub[1], data,  auth=creds)

# CASE: limit reached for from param
print "\n\n"
print "-----------------------  limit reached   -------------------------"

numbers = ["441224980093", "441887480051", "441873440028", "441873440017", "441970450009", "441235330075", "441235330053", "441235330044", "441235330078", "34881254103", "61871112946", "61871112915", "61881666904 4924195509196", "4924195509197", "4924195509195", "4924195509049", "4924195509012", "4924195509193", "4924195509029", "4924195509192", "4924195509194", "31297728125", "3253280312", "3253280311", "3253280315", "3253280313", "3253280329", "441224459508", "441224980086", "441224980087", "441224980096", "441224980098", "441224980099", "441224980100", "441224980094", "441224459426", "13605917249", "61881666939", "61871112913", "61871112901", "61871112938", "61871112934", "61871112902", "61881666926", "61871705936", "61871112920", "61881666923", "61871112947", "61871112948", "61871112921", "61881666914", "61881666942"]

for number in numbers:
    print "inbound sms"
    data = {"from": "61871112913", "to": number, "text": "Lets STOP the chat."}
    sendRequest(url_hub[0], data,  auth=creds)

