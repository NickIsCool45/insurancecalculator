import requests, json

def getCounty(zip):
    params = {
        'apikey': 'd687412e7b53146b2631dc01974ad0a4'
    }
    response = requests.get('https://marketplace.api.healthcare.gov/api/v1/counties/by/zip/' + str(zip),
                            params=params)
    return response.json()["counties"][0]["name"][:-7]

def getFips(zip):
    params = {
        'apikey': 'd687412e7b53146b2631dc01974ad0a4'
    }
    response = requests.get('https://marketplace.api.healthcare.gov/api/v1/counties/by/zip/' + str(zip),
                            params=params)
    return response.json()["counties"][0]["fips"]
def getState(zip):
    params = {
        'apikey': 'd687412e7b53146b2631dc01974ad0a4'
    }
    response = requests.get('https://marketplace.api.healthcare.gov/api/v1/counties/by/zip/' + str(zip),
                            params=params)
    return response.json()["counties"][0]["state"]
