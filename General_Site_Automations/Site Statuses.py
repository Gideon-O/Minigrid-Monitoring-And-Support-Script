import africastalking
import requests
from datetime import datetime
from pytz import timezone
import math
import re
import smtplib

# Software enabled solution to automatically check and report via SMS
# and email on:
# - The status of each site
# - The credit balance for Bulk SMS provider account
class SparkData:
    '''Used to get various site ground information'''
    '''Option 1 using the first three characters of customer code'''
    def __init__(self, customer_code):
        self.customer_code = customer_code

    def base_url(self):
        '''Determine the base url to call from the customer's code first three characters'''
        '''Return a base url to headers function if successful, otherwise raise an error'''
        if self.customer_code[:3].upper() == "LON":
            base_url = "https://nal-longech-site.sparkmeter.cloud/api/v0/"
            return base_url
        elif self.customer_code[:3].upper() == "DUK":
            base_url = "https://nal-dukana.sparkmeter.cloud/api/v0/"
            return base_url
        elif self.customer_code[:3].upper() == "LOL":
            base_url = "https://nal-lolupe.sparkmeter.cloud/api/v0/"
            return base_url
        elif self.customer_code[:3].upper() == "ILL":
            base_url = "https://nal-illeret.sparkmeter.cloud/api/v0/"
            return base_url
        else:
            return "please enter correct customer code"

    def headers(self):
        '''If the characters match, avail log in credentials to the make_request function'''

        if self.customer_code[:3].upper() == "LON":
            headers_longech = {'Content-Type': 'application/json',
                               'Authentication-Token': '''Site server authentication token'''}
            return headers_longech
        elif self.customer_code[:3].upper() == "DUK":
            headers_dukana = {'Content-Type': 'application/json',
                              'Authentication-Token': '''Site server authentication token'''}
            return headers_dukana
        elif self.customer_code[:3].upper() == "LOL":
            headers_lolupe = {'Content-Type': 'application/json',
                              'Authentication-Token': '''Site server authentication token'''}
            return headers_lolupe
        elif self.customer_code[:3].upper() == "ILL":
            headers_illeret = {'Content-Type': 'application/json',
                               'Authentication-Token': '''Site server authentication token'''}
            return headers_illeret
        else:
            print("please enter correct customer code")

    def make_request(self, method, endpoint):
        '''Attempting a ping request to the ground servers via the cloud'''
        if method == "GET":
            try:
                response = requests.get(self.base_url() + endpoint, headers=self.headers())
            except Exception as e:
                return "Connection error while making %s request to %s:%s", method, endpoint, e

        elif method == "POST":
            try:
                response = requests.post(self.base_url() + endpoint, headers=self.headers())
            except Exception as e:
                return "Connection error while making %s request to %s:%s", method, endpoint, e
        else:
            raise ValueError()

        if response.status_code == 200:
            return response.json()
        else:
            if response.json()['status'] == 'success':
                return "Action Successful"
            else:
                return "Error while making %s request to %s: %s(error code %s)", method, self.base_url() + endpoint, \
                       response.json(), response.status_code

    def system_info(self):
        '''Get the specific site status information'''
        endpoint = "system-info"
        response_obj = self.make_request("GET", endpoint=endpoint)
        return response_obj

def kataboi_online():
    '''Function to check the online status of Kataboi site'''
    '''This is based on ami.calinhost.com platoform'''
    data = {
        "CompanyName": "CompanyName",
        "UserName": "UserName",
        "Password": "Password",
    }
    Kataboi = 'DCU Serial Number'
    Nadwat = 'DCU Serial Number'
    base_url = "http://ami.calinhost.com"
    endpoint = "/api/COMM_OnlineStatus"
    response = requests.post(base_url + endpoint, data)
    try:
        status = response.json()['Result'][-1]['Status']
        if status == True:
            return "KAT is Online"
        else:
            return "KAT is Offline"
    except:
        return "KAT Error"


def nadwat_online():
    '''Function to check the online status of Kataboi site'''
    '''This is based on ami.calinhost.com platoform'''
    data = {
        "CompanyName": "CompanyName",
        "UserName": "UserName",
        "Password": "Password",
    }
    Kataboi = 'DCU Serial Number'
    Nadwat = 'DCU Serial Number'
    base_url = "http://ami.calinhost.com"
    endpoint = "/api/COMM_OnlineStatus"
    response = requests.post(base_url + endpoint, data)

    try:
        status = response.json()['Result'][0]['Status']
        if status == True:
            return "NAD is Online"
        else:
            return "NAD is Offline"
    except:
        return "NAD Error"

# Function to sync script time with system time.
def run_sites(site):
    global last_sync
    current_time = datetime.now()
    #  sites = ['DUK', 'LON', 'ILL', 'LOL']
    for content in SparkData(site).system_info()['grids']:
        last_sync = content['last_sync_date']
        last_sync = last_sync.replace(last_sync[10], " ")
        nlast_sync = int(last_sync[11:13]) + 3
        nlast_sync = str(nlast_sync)
        # last_sync = last_sync.replace(last_sync[11:13], nlast_sync)
        last_sync = last_sync[0:19]
        last_sync = datetime.strptime(last_sync, '%Y-%m-%d %H:%M:%S')
        # print("%s sync time is %s " % (abbre, last_sync))
        tim_diff = current_time - last_sync

        diff_in_seconds = int(tim_diff.total_seconds()) - 3600 * 3

        secs_yr = 31536000
        secs_mnth = 2592000
        secs_day = 86400
        secs_hour = 3600
        secs_min = 60

        current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        year_diff = diff_in_seconds / secs_yr
        month_diff = diff_in_seconds / secs_mnth  # MONTH DIFFENCE
        day_diff = diff_in_seconds / secs_day  # DAY DIFFENCE
        hour_diff = diff_in_seconds / secs_hour  # HOUR DIFFENCE
        minute_diff = diff_in_seconds / secs_min  # MINUTE DIFFENCE

        if year_diff > 1:
            un_year_diff = year_diff
            year_fractional, whole = math.modf(un_year_diff)
            year_diff = un_year_diff - year_fractional
            un_month_diff = round(12 * ((diff_in_seconds % secs_yr) / secs_yr), 4)
            month_fractional, whole = math.modf(un_month_diff)
            month_diff = un_month_diff - month_fractional
            un_day_diff = month_fractional * 30
            day_fractional, whole = math.modf(un_day_diff)
            day_diff = un_day_diff - day_fractional
            un_hour_diff = day_fractional * 24
            hour_fractional, whole = math.modf(un_hour_diff)
            hour_diff = un_hour_diff - hour_fractional
            un_minute_diff = hour_fractional * 60
            minute_fractional, whole = math.modf(un_minute_diff)
            minute_diff = un_minute_diff - minute_fractional
            return "%s is offline for: %s  year(s), %s month(s), %s day(s), %s  hour(s) %s  min(s)" % (site,
                                                                                                       year_diff,
                                                                                                       month_diff,
                                                                                                       day_diff,
                                                                                                       hour_diff,
                                                                                                       minute_diff)
        elif year_diff < 1:
            if month_diff > 1:
                un_month_diff = month_diff
                month_fractional, whole = math.modf(un_month_diff)
                month_diff = un_month_diff - month_fractional
                un_day_diff = month_fractional * 30
                day_fractional, whole = math.modf(un_day_diff)
                day_diff = un_day_diff - day_fractional
                un_hour_diff = day_fractional * 24
                hour_fractional, whole = math.modf(un_hour_diff)
                hour_diff = un_hour_diff - hour_fractional
                un_minute_diff = hour_fractional * 60
                minute_fractional, whole = math.modf(un_minute_diff)
                minute_diff = un_minute_diff - minute_fractional
                return "%s is offline for : %s month(s)  %s day(s)  %s hour(s) %s min(s)" % (site,
                                                                                             month_diff, day_diff,
                                                                                             hour_diff, minute_diff)
            elif month_diff < 1:
                if day_diff > 1:
                    un_day_diff = day_diff
                    day_fractional, whole = math.modf(un_day_diff)
                    day_diff = un_day_diff - day_fractional
                    un_hour_diff = day_fractional * 24
                    hour_fractional, whole = math.modf(un_hour_diff)
                    hour_diff = un_hour_diff - hour_fractional
                    un_minute_diff = hour_fractional * 60
                    minute_fractional, whole = math.modf(un_minute_diff)
                    minute_diff = un_minute_diff - minute_fractional
                    return "%s is offline for: %s day(s) %s hour(s) %s min(s)" % (site,
                                                                                  day_diff, hour_diff, minute_diff)
                elif day_diff < 1:
                    if hour_diff > 1:
                        un_hour_diff = hour_diff
                        hour_fractional, whole = math.modf(un_hour_diff)
                        hour_diff = un_hour_diff - hour_fractional
                        un_minute_diff = hour_fractional * 60
                        minute_fractional, whole = math.modf(un_minute_diff)
                        minute_diff = un_minute_diff - minute_fractional
                        return "%s is Offline" % site
                    # return "%s is offline for: %s hour(s) %s min(s)" % (site, hour_diff, minute_diff)
                    elif hour_diff < 1:
                        if minute_diff > 30:
                            un_minute_diff = minute_diff
                            minute_fractional, whole = math.modf(un_minute_diff)
                            minute_diff = un_minute_diff - minute_fractional
                            return "%s is Offline" % site
                        # return "%s is offline for: %s min(s)" % (site, minute_diff)
                        elif minute_diff < 30:
                            return "%s is Online" % site

# Function to check for dukana online connectivity
def check_dukana_online_status():
    sites = ['DUK']
    for items in sites:
        return run_sites(items)

# Function to check for ileret online connectivity
def check_illeret_online_status():
    sites = ['ILL']
    for items in sites:
        return run_sites(items)

# Function to check for lolupe online connectivity
def check_lolupe_online_status():
    sites = ['LOL']
    for items in sites:
        return run_sites(items)

# Function to check for longech online connectivity
def check_longech_online_status():
    sites = ['LON']
    for items in sites:
        return run_sites(items)


# Class to send SMS, calls all the other classes and functions
class SendSms():

    # TODO: Initialize Africa's Talking
    def __init__(self):
        self.username = 'username'
        self.api_key = 'Your API Key'

    # TODO: Send message
    def sending_not_all_online(self):
        current_time = datetime.now(timezone('Africa/Nairobi')).strftime('%Y-%m-%d %H:%M')
        africastalking.initialize(self.username, self.api_key)
        # Set the numbers in international format
        recipients = ["+254729702990", "+254728124536", "+254708871348"]
        # Set your message
        message = " As at %s \n1. %s  \n2. %s     \n3. %s      \n4. %s    \n5. %s   \n6. %s  " % (
            current_time, check_longech_online_status(),
            check_lolupe_online_status(),
            check_illeret_online_status(),
            check_dukana_online_status(), nadwat_online(), kataboi_online())

        #SEND EMAIL NOTIFICATION BELOW
        fromaddr = 'brian@nal.co.ke'
        to_jevel = 'kakamijevel@gmail.com'
        to_technical = 'technical@nal.co.ke'

        msg = "\r\n".join(["From:" "NAL Offgrid Informer",
                           "To:" + to_jevel,
                           "Cc:" + to_technical,
                           "Subject: Status of Sites",
                           "",
                           "Dear Jevel,\n",
                           " As at %s \n 1. %s  \n 2. %s \n 3. %s \n 4. %s  " % (
                               current_time, check_longech_online_status(),
                               check_lolupe_online_status(), nadwat_online(), kataboi_online()),
                           "\n"
                           "Please contact caretakers for the sites appearing to be offline and confirm if the sites "
                           "are "
                           "'ON' or 'OFF'.\n"
                           "In case of a technical issue beyond your ability to resolve, please contact Brian for "
                           "further guidance\n"
                           "\n"
                           "Best regards\n"
                           "AUTO_NAL"
                           ])
        username = fromaddr
        password = 'naloffgrid2022'

        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(username, password)
            server.sendmail(fromaddr, to_jevel, msg)
            server.sendmail(fromaddr, to_technical, msg)
            server.quit()
            print("EMAIL SENT")

        except Exception as e:
            print("The following error was encountered; \n"
                  "%s" % e)

        # Set your shortCode or senderId
        # SEND SMS NOTIFICATION
        sender = "NAL_OFFGRID"
        try:
            response = africastalking.SMS.send(message, recipients, sender)
            feedback = response['SMSMessageData']['Recipients'][0]['status']
            if feedback == "InsufficientBalance": # This is where I initiate email to accounts to top-up accounts
                print("Hello Brian No Balance on Africa's talking")
        except Exception as e:
            print(f'Brian, we have a problem: {e}')

    def sending_all_online(self):
        lon = check_longech_online_status()
        lol = check_lolupe_online_status()
        ill = check_illeret_online_status()
        duk = check_dukana_online_status()
        nad = nadwat_online()
        kat = kataboi_online()
        longech = re.search("Online$", lon)
        if longech:
            lolupe = re.search("Online$", lol)
            if lolupe:
                illeret = re.search("Online$", ill)
                if illeret:
                    dukana = re.search("Online$", duk)
                    if dukana:
                        nadwat = re.search("Online$", nad)
                        if nadwat:
                            kataboi = re.search("Online$", kat)
                            if kataboi:
                                current_time = datetime.now(timezone('Africa/Nairobi')).strftime('%Y-%m-%d %H:%M')
                                africastalking.initialize(self.username, self.api_key)
                                # Set the numbers in international format
                                recipients = ["+254729702990", "+254728124536", "+254708871348"]
                                # Set your message
                                message = " As at %s \n Hurray! All sites are Online" % current_time
                                # Set your shortCode or senderId
                                sender = "NAL_OFFGRID"
                                try:
                                    response = africastalking.SMS.send(message, recipients, sender)
                                    print(response)
                                    print("This is the Error Above")
                                except Exception as e:
                                    print(f'Brian, we have a problem: {e}')
                            else:
                                return self.sending_not_all_online()
                        else:
                            return self.sending_not_all_online()
                    else:
                        return self.sending_not_all_online()
                else:
                    return self.sending_not_all_online()
            else:
                return self.sending_not_all_online()
        else:
            return self.sending_not_all_online()

# Initialize the class and call the function
SendSms().sending_all_online()
