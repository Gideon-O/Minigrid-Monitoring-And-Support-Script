# sparkmeter imports
import requests
import json

# datetime imports
from datetime import timedelta, date
import datetime

# africastalking imports
import africastalking as at

# Initializing africastalking saga'''
'''Credntials for Africastalking API'''
username = "username"
api_key = "Bulk SMS API Key"

'''Initialization of the API'''
at.initialize(username, api_key)
sms = at.SMS

# Initializing the date time file'''
'''Open the file so as read the balance dates date'''
open_balance_date_file = open(r"/home/Gideon2O/nal_offgrid_sites/trial_sales/balance_dates.txt", "r")
balance_date_today = open_balance_date_file.readline(10)
balnce_date_today_formatted = datetime.datetime.strptime(balance_date_today, "%Y-%m-%d")
balance_working_date = balnce_date_today_formatted
open_balance_date_file.close()

'''Open the file so as read the negative balance dates date'''
open_negative_date_file = open(r"/home/Gideon2O/nal_offgrid_sites/trial_sales/negative_dates.txt", "r")
negative_date_today = open_negative_date_file.readline(10)
negative_date_today_formatted = datetime.datetime.strptime(negative_date_today, "%Y-%m-%d")
negative_working_date = negative_date_today_formatted
open_negative_date_file.close()

# A function that checks if the date today is similar to the date in file
# If the dates a similar, it calls the send message function, and updates the date is file
# Otherwise, pass
def check_update_dates():
    global date_today, balance_working_date, negative_working_date
    '''Get the current day, combine with min time to have it matching with the strptime result'''
    present_day_date = datetime.date.today()
    min_time = datetime.datetime.min.time()
    present_day_min_datetime = datetime.datetime.combine(present_day_date, min_time)

    if present_day_min_datetime == balance_working_date:
        '''Advance the dates by 3 days every time the the customers are reminded'''
        balance_working_date = balance_working_date + timedelta(days=3)
        '''Convert the working_date to a string format'''
        advance_balance_date = datetime.datetime.strftime(balance_working_date, "%Y-%m-%d")
        '''Open file to update the predefined date for future alerts'''
        write_balance_date = open(r"/home/Gideon2O/nal_offgrid_sites/trial_sales/balance_dates.txt", "w")
        write_balance_date.write(advance_balance_date)
        write_balance_date.close()

        '''Call the function that checks for customer credit balance'''
        print("Balance reminder dates updated")
        collect_customer_balance()

    if present_day_min_datetime == negative_working_date:
        '''Advance the dates by 6 days every time the customers are reminded'''
        negative_working_date = negative_working_date + timedelta(days=6)
        '''Convert the negative working date to a string format'''
        advance_negative_date = datetime.datetime.strftime(negative_working_date, "%Y-%m-%d")
        '''Open the date file to update the predefined date for future alarts'''
        write_negative_date = open(r"/home/Gideon2O/nal_offgrid_sites/trial_sales/negative_dates.txt", "w")
        write_negative_date.write(advance_negative_date)
        write_negative_date.close()

        '''Call for the function that checks for significantly negative credit balance'''
        print("Huge negative dates updated")
        collect_negative_customer_balance()

    else:
        print("Not yet the day")

# A function that collects customer information i.e., balances and phone number
def collect_customer_balance():
    url = "https://nal-illeret.sparkmeter.cloud/api/v0/customers"
    payload={}
    headers = {
        'Content-Type':'application/json',
        'Authentication-Token': '''Authentication token''',
    }
    response = requests.request("GET", url, headers=headers, data=payload).json()
    customer_list = response['customers']
    count = 0

    '''Loops through each customer and checks if balance is below 10'''
    for customer in range(len(customer_list)):
        customer = customer_list[count]
        code = customer['code']
        balance = round(customer['credit_balance'])
        number = customer['phone_number']
        #print(count)
        if number is not None:
            phone_number = number.strip()
            if balance < 20 and balance > -10:
                message = "Customer: " + code + "\nCredit balance: " + str(balance) + "\nLipia stima sasa kabla credit iishe.\nPAYBILL: 820400\n\nNAL OFFGRID LTD"
                send_message(phone_number, message)
            else:
                print("You're all set!")

        else:
            pass

        count = count + 1

def collect_negative_customer_balance():
    url = "https://nal-illeret.sparkmeter.cloud/api/v0/customers"
    payload={}
    headers = {
        'Content-Type':'application/json',
        'Authentication-Token': '''Authentication token''',
    }
    response = requests.request("GET", url, headers=headers, data=payload).json()
    customer_list = response['customers']
    count = 0

    '''Loops through each customer and checks if balance is below 20'''
    for customer in range(len(customer_list)):
        customer = customer_list[count]
        code = customer['code']
        balance = round(customer['credit_balance'])
        number = customer['phone_number']
        #print(count)
        if number is not None:
            phone_number = number.strip()
            if balance < -10:
                '''Include code for endmonth and mid-month'''
                message = "Customer: " + code + "\nCredit balance: " + str(balance) + "\nTafuta CARETAKER akupe usaidizi.\n\nNAL OFFGRID LTD"
                send_message(phone_number, message)
            else:
                print("You're all set!")

        else:
            pass

        count = count + 1


def send_message(phone_number, message):
    recipient = [phone_number]
    try:
            response = sms.send(message, recipient)
            print("Message Sent")
    except Exception as e:
            print(f'Engineer, there\'s an a problem\n{e}')

# Initialize the whole script by calling the check_update_date function
check_update_dates()