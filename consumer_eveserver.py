import requests.packages.urllib3
import evelink.server
import sys
from time import sleep
from _eveserver import *

requests.packages.urllib3.disable_warnings()

def main():
    service = "consumer_eveserver.py"

    serverapi = evelink.server.Server()
    serverapiresponse = serverapi.server_status()
    serverapi_data = serverapiresponse.result
    serverapi_cachedUntil = arrow.get(serverapiresponse.timestamp)
    servertimestamp = serverapi_cachedUntil.format('YYYY-MM-DD HH:mm:ss')

    players = serverapi_data['players']
    status = serverapi_data['online']

    eveserver_insertstatus(servertimestamp, players, status)

if __name__ == "__main__":
    main()

    # Sleep for 30 minutes before ending and triggering another run via supervisor
    print("[Completed Run:Sleeping for 2 Minutes]")
    sys.stdout.flush()
    sleep(120)
