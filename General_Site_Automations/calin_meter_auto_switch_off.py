import requests

# Class to automatically switch on a Smart Calin Meter remotely at specified time
# Target platform: Calin meter's www.ami.calinhost.com
class CalinMeterOff:
    def __init__(self):
        self.base_url = "http://ami.calinhost.com/api"


    # A function to log in into the platform
    def meter_off_code(self):
        data = {'CompanyName': "CompanyName",
                'UserName': "UserName",
                'Password': "Password",
                'MeterNo': "MeterNo",
                'DataItem': 'switch off'
        }
        endpoint = "/COMM_RemoteControl"
        response = requests.post(self.base_url + endpoint, data)
        return response.json()['Result']['TaskNo']
    
    # Function to do the actual switching off.
    def switch_meter_off(self):
        data = {'CompanyName': "CompanyName",
                'UserName': "UserName",
                'Password': "Password",
                'TaskNo': self.meter_off_code()
        }
        endpoint = "/COMM_RemoteControlTask"
        response = requests.post(self.base_url + endpoint, data)
        return response.json()

# Initialize the CalinMeterOff class and call switch_off function
CalinMeterOff().switch_meter_off()