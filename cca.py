from datetime import datetime
import requests
from countyGET import getCounty

url = "https://coveredcalifornia-calculator-api.azurewebsites.net/api/subsidy-calculator/calculate"
header = {
    "Content-Type": "application/json",
    "Priority": "u=1, i",
    "Origin": "https://www.coveredca.com"
}

def get_cca(json_data):
    coverage_year = datetime.now().year
    coverage_year = "2024"
    county = getCounty(json_data["applicant"]["zip"])
    zip_code = json_data["applicant"]["zip"]
    household_income = json_data["householdIncome"]
    household_size = 1 + len(json_data["family"])
    household_ages = [json_data["applicant"]["age"]] + [member["age"] for member in json_data["family"]]

    payload = {
        "formValues": {
            "coverageYear": coverage_year,
            "zip": str(zip_code),
            "county": county,
            "householdSize": str(household_size),
            "householdIncome": str(household_income),
            "householdMembers": household_ages,
            "didReceiveUnemploymentInsurance": False
        }
    }
    res = requests.post(url, headers=header, json=payload)
    if res.status_code != 200:
        print("CoveredCA Insurance Plans Failed! Exit Code: " + str(res.status_code))
        return res.status_code

    data = res.json()
    plans = {
        "Covered California Bronze": float(data.get('lowestBronzeRate', None)),
        "Covered California Silver": float(data.get('secondLowestSilverRate', None))
    }
    return plans