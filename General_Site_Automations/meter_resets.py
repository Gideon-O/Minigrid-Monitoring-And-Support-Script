from lib2to3.pgen2 import token
import requests
import json

payload={}

# Parent class with the various functions for each site.
class MeterReset:
    def __init__(self) -> None:
        pass

    def reset_longech(self):
        site = "nal-longech-site"
        token = '''Authentication token'''
        url = "https://" + site + ".sparkmeter.cloud/api/v0/customers"
        payload={}
        headers = {
            'Content-Type': 'application/json',
            'Authentication-Token': token
        }

        # Returns a json data file containing all the customers, and their details
        response = requests.request("GET", url, headers=headers, data=payload).json()

        # Isolates the 'customers' attribute only.
        customer_list = response['customers']

        # Loop through each of the customers returned and obtain the internal customer ID
        # Initialize x that will be used for incrementing through the customer
        x = 0
        for customer in range(len(customer_list)):
            #print(str(x) + ":")
            customer_internal_id = customer_list[x]['id']

            # Reset the meter
            url = "https://"+site+".sparkmeter.cloud/api/v0/customers/"+customer_internal_id+"/reset-meter"
            payload = {}
            headers = {
                'Authentication-Token': token
            }

            meter_reset = requests.request("POST", url, headers=headers, data=payload)
            print('id: ' + customer_internal_id)
            print(meter_reset.text)
            x = x + 1

    def reset_lolupe(self):
        site = "nal-lolupe"
        token = '''Authentication token'''
        url = "https://" + site + ".sparkmeter.cloud/api/v0/customers"
        payload={}
        headers = {
            'Content-Type': 'application/json',
            'Authentication-Token': token
        }

        # Returns a json data file containing all the customers, and their details
        response = requests.request("GET", url, headers=headers, data=payload).json()

        # Isolates the 'customers' attribute only.
        customer_list = response['customers']

        # Loop through each of the customers returned and obtain the internal customer ID
        # Initialize x that will be used for incrementing through the customer
        x = 0
        for customer in range(len(customer_list)):
            #print(str(x) + ":")
            customer_internal_id = customer_list[x]['id']

            # Reset the meter
            url = "https://"+site+".sparkmeter.cloud/api/v0/customers/"+customer_internal_id+"/reset-meter"
            payload = {}
            headers = {
                'Authentication-Token': token
            }

            meter_reset = requests.request("POST", url, headers=headers, data=payload)
            print('id: ' + customer_internal_id)
            print(meter_reset.text)
            x = x + 1

    def reset_illeret(self):
        site = "nal-illeret"
        token = '''Authentication token'''
        url = "https://" + site + ".sparkmeter.cloud/api/v0/customers"
        payload={}
        headers = {
            'Content-Type': 'application/json',
            'Authentication-Token': token
        }

        # Returns a json data file containing all the customers, and their details
        response = requests.request("GET", url, headers=headers, data=payload).json()

        # Isolates the 'customers' attribute only.
        customer_list = response['customers']

        # Loop through each of the customers returned and obtain the internal customer ID
        # Initialize x that will be used for incrementing through the customer
        x = 0
        for customer in range(len(customer_list)):
            #print(str(x) + ":")
            customer_internal_id = customer_list[x]['id']

            # Reset the meter
            url = "https://"+site+".sparkmeter.cloud/api/v0/customers/"+customer_internal_id+"/reset-meter"
            payload = {}
            headers = {
                'Authentication-Token': token
            }

            meter_reset = requests.request("POST", url, headers=headers, data=payload)
            print('id: ' + customer_internal_id)
            print(meter_reset.text)
            x = x + 1

    def reset_dukana(self):
        site = "nal-dukana"
        token = '''Authentication token'''
        url = "https://" + site + ".sparkmeter.cloud/api/v0/customers"
        payload={}
        headers = {
            'Content-Type': 'application/json',
            'Authentication-Token': token
        }

        # Returns a json data file containing all the customers, and their details
        response = requests.request("GET", url, headers=headers, data=payload).json()

        # Isolates the 'customers' attribute only.
        customer_list = response['customers']

        # Loop through each of the customers returned and obtain the internal customer ID
        # Initialize x that will be used for incrementing through the customer
        x = 0
        for customer in range(len(customer_list)):
            #print(str(x) + ":")
            customer_internal_id = customer_list[x]['id']

            # Reset the meter
            url = "https://"+site+".sparkmeter.cloud/api/v0/customers/"+customer_internal_id+"/reset-meter"
            payload = {}
            headers = {
                'Authentication-Token': token
            }

            meter_reset = requests.request("POST", url, headers=headers, data=payload)
            print('id: ' + customer_internal_id)
            print(meter_reset.text)
            x = x + 1


# initialize the class by assigning it to a variable
resets = MeterReset()

# call various sites and reset for each customer
resets.reset_longech()
resets.reset_lolupe()
resets.reset_illeret()
resets.reset_dukana()