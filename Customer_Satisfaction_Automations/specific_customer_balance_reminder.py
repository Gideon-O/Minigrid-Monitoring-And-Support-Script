import requests
import json
from datetime import date
import africastalking as at
import os
from urllib import response
from email import message


# Function to the check the balance for Customer
# Reminds the customer daily on the remaining balance if it is below a set
# threshold of Kshs. 100
def check_balance():
    url = "https://nal-longech-site.sparkmeter.cloud/api/v0/customer/{customer_code}"

    token = '''Authentication token for the specific site'''

    payload = {}
    headers = {
                'Content-Type': 'application/json',
                'Authentication-Token': token
            }

    response = requests.request("GET", url, headers=headers, data=payload).json()
    balance = response['customers'][0]['credit_balance']
    account = response['customers'][0]['code']
    phone_number = response['customers'][0]['phone_number']

    '''Print the customer balance here'''
    # print(account)
    # print(balance)

    '''Call function to check for Threshold'''
    threshold(balance, account, phone_number)

# Function to check if balance is below threshold
def threshold(balance, account, phone_number):
    if balance < 100:
        send_SMS(balance, account, phone_number)
    else:
        print("Balance iko sawa")


# Function to send SMS
def send_SMS(balance, account, phone_number):
    '''Credntials for Africastalking API'''
    username = "username"
    api_key = '''Your Africastalking API'''

    '''Initialization of the API'''
    at.initialize(username, api_key)
    sms = at.SMS

    '''Round off the balance to the nearest whole number and convert to string'''
    bal = str(round(balance))

    number = phone_number.strip()
    recipient = [number]
    #alert = "Dear Customer, we introduced an alert for your credit balance when below Kshs. 100, once a day.The alert will be as below:\n\n"
    message = "Customer Account: "+ account +"\nCredit-Balance: "+ bal +"\nRecharge before depletion to avoid inconveniences.\n\nNal Off-grid"

    try:
            response = sms.send(message, recipient)
            print("Message Sent")
    except Exception as e:
            print(f'Engineer, there\'s an a problem\n{e}')

# Call function that activates all the other functions
check_balance()