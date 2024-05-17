import requests, json
from datetime import datetime
from countyGET import getCounty

def dob_from_age(age):
  dobString = "{year}-{month}-{day}"
  dobString = dobString.format(year=datetime.now().year-age, month="%02d" % datetime.now().month, day="%02d" % datetime.now().day)
  return dobString

def getServiceArea(zip, year):
  headers = {
    'lob': 'kpif',
    'planyear': str(year),
    'x-env': 'prod',
    'zipcode': str(zip),
  }
  res = requests.get('https://apims.kaiserpermanente.org/kp/care/jkp-sp/v1/shop-plans/servicearea', headers=headers)
  return res.json()


def get_kaiser(data):
  coverage_year = datetime.now().year
  zip_code = data["applicant"]["zip"]
  county = getCounty(zip_code)
  household_income = data["householdIncome"]
  dob = dob_from_age(int(data["applicant"]["age"]))

  serviceAreaJson = getServiceArea(zip_code, coverage_year)
  members = [{
    "id":1,
    "relationship":"self",
    "dateOfBirth":dob
  }]
  id = 2
  for member in data["family"]:
    if member["relationship"] == "child":
      members.append({
        "id":id,
        "relationship":"dependant",
        "dateOfBirth":dob_from_age(int(member["age"]))
      })
    elif member["relationship"] == "spouse":
      members.append({
        "id":id,
        "relationship":"spouse",
        "dateOfBirth":dob_from_age(int(member["age"]))
      })
    id+=1
  headers = {
    'content-type':'application/json; charset=UTF-8',
    'lob':'kpif',
    'plan_language':'en',
    'x-appname':'jkp-shopplans-kpif',
    'x-env':'prod'
  }
  payload = {
    "onHix":serviceAreaJson["servicearea"][0]["isOnHix"],
    "offHix":serviceAreaJson["servicearea"][0]["isOffHix"],
    "lob":"kpif",
    "zipcode":str(zip_code),
    "county":county,
    "effectiveDate":serviceAreaJson["effectivedate"],
    "enrollmentYear":str(coverage_year),
    "state":serviceAreaJson["servicearea"][0]["state"],
    "subregion":serviceAreaJson["servicearea"][0]["subregion"],
    "servicearea":serviceAreaJson["servicearea"][0]["county"],
    "persons":members,
    "annualHouseholdIncome":str(household_income),
    "taxableHouseholdSize":str(len(members))
  }
  res = requests.post("https://apims.kaiserpermanente.org/kp/care/jkp-sp/v1/shop-plans/kpif/plans", json=payload, headers=headers)
  if res.status_code != 200:
    print("Kaiser Insurance Plans Failed! Exit Code: " + str(res.status_code))
    return res.status_code
  data = res.json()
  plans = {}
  for plan in data["plans"]:
    plans.update({plan["plan"]["planname"]:float(plan["plan"]["rate"]["totalRate"])})
  return plans
  