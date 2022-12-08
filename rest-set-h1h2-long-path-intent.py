import requests
import urllib.parse
import json
from requests.auth import HTTPBasicAuth

ONE="0A:00:00:00:00:01"
TWO="0A:00:00:00:00:02"


def create_intent(ONE,TWO):
    # we are using a url so need to encode (and it needs /-1 at the end)
    h1=urllib.parse.quote_plus(ONE+"/-1")
    h2=urllib.parse.quote_plus(TWO+"/-1")
    # now get the disjoint paths
    try:
        r=requests.get("http://127.0.0.1:8181/onos/v1/paths/"+h1+"/"+h2+"/disjoint",auth=HTTPBasicAuth('onos', 'rocks'))
    except requests.exceptions.RequestException as e:
        print("Error getting hosts "+e)
        exit(1)
    r=r.json()
    # the backup path is the longer path
    path=r['paths'][0]['backup']['links']
    # iterate through the path to get the in/out device/port
    for i in range(len(path)-1):
        device=path[i]['dst']['device']
        inport=path[i]['dst']['port']
        outport=path[i+1]['src']['port']
        # we have the information, now create a dict for the API
        data={
            "type": "PointToPointIntent",
            "appId": "org.onosproject.ovsdb",
            "priority": 55,
            "selector": {"criteria": [{"type": "ETH_SRC",
                          "mac": ONE},
                         {"type": "ETH_DST",
                          "mac": TWO}]},
            "ingressPoint": {
                "port": inport,
                "device": device
            },
            "egressPoint": {
                "port": outport,
                "device": device
            }
        }
        # tell the controller to install the "intent"
        try:
            r=requests.post("http://127.0.0.1:8181/onos/v1/intents/",auth=HTTPBasicAuth('onos', 'rocks'),json=data)
        except requests.exceptions.RequestException as e:
            print("Error setting intent "+e)
            exit(1)
        print(data)
# create intent in the forward direction
create_intent(ONE,TWO)
# and then the reverse
create_intent(TWO,ONE)
