#!/usr/bin/python
import re
import datetime
import subprocess

#  get time
time_now = datetime.datetime.now()

#  get time in same format at /var/log/messages
time_now_time = time_now.strftime('%b %d %H:%M')

#  get time - 10 mins in same format as /var/log/messages
time_now_mins_10 = time_now - datetime.timedelta(minutes = 10)
time_now_mins_10 = time_now_mins_10.strftime('%b %d %H:%M')

#  get time - 24 hours (1440 mins) in same format as /var/log/messages
time_now_mins_1440 = time_now - datetime.timedelta(minutes = 1440)
time_now_mins_1440 = time_now_mins_1440.strftime('%b  %-d %H:')

# get time - 23 hours (1380) in same format as /var/log/messages
time_now_mins_1380 = time_now - datetime.timedelta(minutes = 1380)
time_now_mins_1380 = time_now_mins_1380.strftime('%b  %-d %H:')


def check_10min_occurences(time_now_mins_1380, time_now_mins_1440):
        get_logger_entry = "Service was restarted on"
        search_file = False
        with open("/var/log/messages", "r") as inFile:
                count = 0
                for line in inFile:
                        line = line.strip()
                        if search_file:                       # if true, search remaining lines in file
                                if get_logger_entry in line:  # check to see if the line matches a monit restart
                                        count += 1            # if it matches, add 1 to the counter
                        elif time_now_mins_1380 in line or time_now_mins_1440 in line:        # check 23 hour and 24 hours worth of logs via the time stamp
                                 search_file = True           # start checking the the logs once the time stamp matches
        return count



curl_response = subprocess.call(["curl --output /dev/null --silent --head --fail -k --connect-timeout 30 https://localhost -H 'Host: test.lazyluke.xyz'"], shell=True)

if curl_response > 0:                                          # eg NOT 200 OK
        log_count = check_10min_occurences(time_now_mins_1380, time_now_mins_1440)
        if log_count < 3:                                      # check to see if monit has restarted the service more than 3 times in the last 10 mins
                print "Site down"
                subprocess.call(["sudo -u user -H sh -c '/bin/systemctl restart httpd' "], shell=True)
                subprocess.call(["/usr/bin/logger -s 'MONIT: Service was restarted on ' `date` 2>>/var/log/monit/service.log"], shell=True)  # add a log entry for the restart
        elif log_count >= 3:
                subprocess.call(["/usr/bin/logger -s 'Monit: Service has been restarted more then 3 times in 10 mins - NO action taken' 2>>/var/log/monit/service.log"], shell=True)  # add a log entry for the restart
        else:
                print "Site is Online: no need to restart service"
