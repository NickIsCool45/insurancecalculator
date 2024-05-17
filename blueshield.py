import requests, json
from datetime import datetime
from countyGET import getFips

individualUrl = "https://www.buyblueshieldca.com/api/shopping/plans/?county_code={fips}&coverage_effective_date=2024-06-01&dependants_count=0&ordering=price&year={year}&zipcode={zip}&subscriber_date_of_birth={dob}&market_segment=individual&plan_variation=00&plan_type=medical"
familyUrl = "https://www.buyblueshieldca.com/api/shopping/plans/?county_code={fips}&coverage_effective_date=2024-06-01&dependants_count={dependant_count}&ordering=price&year={year}&zipcode={zip}&subscriber_date_of_birth={dob}{spouse}{dependants}&market_segment=individual&plan_variation=00&plan_type=medical"
spouseString = "&spouse_date_of_birth={dob_spouse}"
dependantString = "&dependant_0_date_of_birth={dob_dependant}"
def dob_from_age(age):
  dobString = "{year}-{month}-{day}"
  dobString = dobString.format(year=datetime.now().year-age, month="%02d" % datetime.now().month, day="%02d" % datetime.now().day)
  return dobString
def get_blueshield(data):
  coverage_year = datetime.now().year
  coverage_year = "2024"
  fips = getFips(data["applicant"]["zip"])
  zip_code = data["applicant"]["zip"]
  dob = dob_from_age(int(data["applicant"]["age"]))
  
  spouse = ""
  dependants = []
  dependantsString = ""
  url = ""
  
  for member in data["family"]:
    if member["relationship"] == "child":
      dependants.append(dob_from_age(int(member["age"])))
    elif member["relationship"] == "spouse":
      spouse = spouseString.format(dob_spouse = dob_from_age(int(member["age"])))
      
  for dependant in dependants:
    dependantsString += dependantString.format(dob_dependant = dependant)

  if spouse == "" and len(dependants) == 0:
    url = individualUrl.format(fips=fips, year=coverage_year, zip=zip_code, dob=dob)
  else:
    url = familyUrl.format(fips=fips, year=coverage_year, zip=zip_code, dob=dob, spouse=spouse, dependant_count = len(dependants), dependants = dependantsString)
  res = requests.get(url)
  if res.status_code != 200:
      print("Blue Shield Insurance Plans Failed! Exit Code: " + str(res.status_code))
      return res.status_code
  data = res.json()
  plans = {}
  for plan in data["results"]:
    price = 0.0
    for member in plan["member_prices"]:
      price += float(plan["member_prices"][member]["price"])
    plans.update({"Blue Shield California: " + plan["display_name"]:price})
  return plans