import requests

# Class to automatically switch on a Smart Calin Meter remotely at specified time
# Target platform: Calin meter's www.ami.calinhost.com
class CalinMeterOn:
    def __init__(self):
        self.base_url = "http://ami.calinhost.com/api"


    # A function to log in into the platform
    def meter_on_code(self):
        data = {'CompanyName': "CompanyName",
                'UserName': "UserName",
                'Password': "Password",
                'MeterNo': "MeterNo",
                'DataItem': 'switch on'
        }
        endpoint = "/COMM_RemoteControl"

        response = requests.post(self.base_url + endpoint, data)

        #return requests.post(self.base_url + endpoint, data)#.json()#['Result']['TaskNo']

        return response.json()['Result']['TaskNo']


    # Function to do the actual switching off.
    def switch_meter_on(self):
        data = {'CompanyName': "CompanyName",
                'UserName': "UserName",
                'Password': "Password",
                'TaskNo': self.meter_on_code()
        }
        endpoint = "/COMM_RemoteControlTask"
        response = requests.post(self.base_url + endpoint, data)
        return response.json()
    
# Initialize the CalinMeterOn class and call switch_on function
CalinMeterOn().switch_meter_on()