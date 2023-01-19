import requests
import sys
import json
from datetime import date


# get data from url and parse to json
def get_data():
    response = requests.get("https://developer-test-339512.ew.r.appspot.com/get-policies/")
    json_data = json.loads(response.text)
    return json_data


# check if "extended" has been passed as argument for extra functionality
def check_if_extended():
    is_extended = False
    if len(sys.argv) > 1:
        is_extended = str(sys.argv[1]) == "extend"
    return is_extended


# calculate if guarantee has expired, and print correct response
def return_guarantee(data, extended):
    try:
        if data['address'] and data['end_date']:
            end_date = date.fromisoformat(data['end_date'])
            days_left = (end_date - date.today()).days
            if days_left >= 0:
                if extended:
                    print(f"Guarantee at address: {data['address']}, is VALID. {days_left + 1} days left.")
                else:
                    print(f"Guarantee at address: {data['address']}, is VALID")
            else:
                if extended:
                    print(f"Guarantee at address: {data['address']}, has ENDED. Ended {-days_left} days ago.")
                else:
                    print(f"Guarantee at address: {data['address']}, has ENDED.")
            return days_left
    except KeyError as error:
        print(f"Guarantee has missing fields: {data}, {error}")
    except ValueError as error:
        print(f"ValueError in JSON Data: {data}, {error}")


def main():
    try:
        json_data = get_data()
        is_extended = check_if_extended()
        for data in json_data:
            return_guarantee(data, is_extended)
    except Exception as error:
        print(error)


if __name__ == '__main__':
    main()
