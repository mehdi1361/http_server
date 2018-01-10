import requests
from datetime import datetime

def main():
    url = "http://192.168.1.149/api/user/player_info/"

    for i in range(1000):
        start_date = datetime.now()
        headers = {
            'authorization': "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1hcyIsInVzZXJfaWQiOjMsImVtYWlsIjoiIiwiZXhwIjoxNTE1NTY4ODMzfQ.IcXcbdfiuzPAb1_fsHuk6vEA8DAAUcVpr-07FM_SAw0",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "782539db-2dcc-b3ee-c326-9387a62ec727"
            }

        response = requests.request("POST", url, headers=headers)
        end_date = datetime.now()

        date_total = end_date - start_date

        print "start_date:{}, end_date:{}, duration:{}".format(start_date, end_date, date_total)

        # print(response.text)


if __name__ == "__main__":
    main()