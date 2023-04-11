# Minigrid-Monitoring-Scripts

This script monitors the status of two categories of sites:
- Sparkmeter integrated sites
- Calin meter integrated sites

With the integration of the hosting platform www.pythonanywhere.com, I always receive hourly SMS notifications on the status of each site i.e.,
1. Site X is Online
2. Site Y is Offline

If the site is offline for more that 24 hours, I start receiving information on how long the site has been offline.

## ALERTS
- I use Africastalking Bulk SMS. They have an easy to use API
- Also, I use gmail API to deliver critical messages such as Low Credit balance
