# Minigrid-Monitoring-Scripts

## General site automation scripts
### A. Site statuses
This script monitors the status of two categories of sites:
- Sparkmeter integrated sites
- Calin meter integrated sites

With the integration of the hosting platform www.pythonanywhere.com, I always receive hourly SMS notifications on the status of each site i.e.,
1. Site X is Online
2. Site Y is Offline

If the site is offline for more that 24 hours, I start receiving information on how long the site has been offline.

### B. Meter resets
This script resets each powered customer meter every day at a specifed time to acknoldge any errors that may have affected the meter over the past 24hrs

### C. Meter auto switch on and off
The script automatically switches a Calin smart meter on/off  based on the time it is set to run on the hosting platform

#### ALERTS
- I use Africastalking Bulk SMS. They have an easy to use API
- Also, I use gmail API to deliver critical messages such as Low Credit balance

## Customer Satisfaction scripts
### A. Specific customer balance reminder
The sript alerts the customer via SMS that their credit balance is below a certain threshold. In this case I set the threshold to Kshs. 100
This reminder is done every day until the customer tops up their electricity token

### B. Site customer balance reminder
The sript alerts the customer via SMS that their credit balance is below a certain threshold. In this case I set the threshold to Kshs. 10
This reminder is done after a specifed interval of days, in this case it is three days.
NOTE:
There are dependent files that contain the allowed and disallowed dates that are frequently updated to ensure the corrent dates are used during the alerting activites.

