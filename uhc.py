import requests, json, datetime
from countyGET import *
from datetime import datetime

url = 'https://www.uhc.com/shop/api/products?'
header = {
    'Accept':'application/json',
    'Referer':'https://www.uhc.com/shop/individuals-families/en/quote/plans/hospitalindemnity?leadsourcename=UHC-IandF&tfn=1-800-557-6718',
    'Request-Id':'|c9b18f1cc96146db93078b1327cbd0d0.99f5cd9e84e14c7a',
    'Requestguid':'D5B210A7-2D5B-E511-80D1-005056BD5356',
    'Sec-Ch-Ua':'"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Mobile':'?0',
    'Sec-Ch-Ua-Platform':"macOS",
    'Traceparent':'00-c9b18f1cc96146db93078b1327cbd0d0-99f5cd9e84e14c7a-01',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}
def dob_from_age(age):
  dobString = "{year}-{month}-{day}"
  dobString = dobString.format(year=datetime.now().year-age, month="%02d" % datetime.now().month, day="%02d" % datetime.now().day)
  return dobString

def get_uhc(json_data):
    zip_code = json_data["applicant"]["zip"]
    applicant = json_data["applicant"]

    payload = {
        'isChildAlone': 'false',
        'paymentModes[]': 'M',
        'applicationType': '',
        'isWindowShopping': 'false',
        'currentDate': dob_from_age(0),
        'quoteSource': 'UHC Store - DTC',
        'applicationSource': 'UHC Store',
        'effectiveDate': dob_from_age(-1),
        'vueBrokerId': '',
        'userType': 'CONSUMER',
        'localeCode': 'en-US',
        'zipCode': zip_code,
        'county': getCounty(zip_code).upper(),
        'countyFipsCode': getFips(zip_code),
        'state': getState(zip_code),
        'applicants[0].applicantTypeCode': 'P',
        'applicants[0].gender': applicant["gender"][0].upper(),
        'applicants[0].isTobacco': applicant["smoker"],
        'applicants[0].birthDate': dob_from_age(applicant["age"]),
        'applicants[0].healthClassName': 'Preferred',
    }
    counter = 1
    for member in json_data["family"]:
       payload.update({
            f'applicants[{counter}].applicantTypeCode': 'P',
            f'applicants[{counter}].gender': member["gender"][0].upper(),
            f'applicants[{counter}].isTobacco': member["smoker"],
            f'applicants[{counter}].birthDate': dob_from_age(member["age"]),
            f'applicants[{counter}].healthClassName': 'Preferred',
       })
    res = requests.get(url, params=payload, headers=header)
    if res.status_code != 200:
        print("UHC Insurance Plans Failed! Exit Code: " + str(res.status_code))
        return res.status_code
    data = res.json()
    result = {
       "UHC Bronze":data[0]["planRates"][0]["rateAmount"],
       "UHC Silver":data[1]["planRates"][0]["rateAmount"],
       "UHC Gold":data[-2]["planRates"][0]["rateAmount"],
       "UHC Platinum":data[-1]["planRates"][0]["rateAmount"]
    }
