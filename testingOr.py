from __future__ import print_function
import re
import requests
from orionsdk import SwisClient

def main():
    npm_server = input('What is the server name: ')
    username = input('What is the username: ')
    password = input('What is the password: ')
    target_node_ip = '10.156.30.5'
    snmpv3_credential_id = 3
    orion_engine_id = 1
    swis = SwisClient(npm_server, username, password)
    print("Discover and add interfaces:")
    results = swis.invoke('Orion.NPM.Interfaces', 'DiscoverInterfacesOnNode', 4)

    # use the results['DiscoveredInterfaces'] for all interfaces
    # or get a subset of interfaces using a comprehension like below
    eth_only = (x for x in results['DiscoveredInterfaces']
                if "Serial" in x["Caption"] or "Gigabit" in x["Caption"])
    
    for x in eth_only:
        print(x["Caption"])

    #print(results)
   # print(eth_only)
'''
    results2 = swis.invoke(
            'Orion.NPM.Interfaces',
            'AddInterfacesOnNode',
            4,                    # use a valid nodeID!
            eth_only,
            'AddDefaultPollers')

    #print(results2)
'''

requests.packages.urllib3.disable_warnings()


if __name__ == '__main__':
    main()