#!/usr/bin/python
import re
import datetime
import subprocess

# get time
time_now = datetime.datetime.now()

#  get time in same format at /var/log/messages
time_now_time = time_now.strftime('%b %d %H:%M')

#  get time - 10 mins in same format as /var/log/messages
time_now_mins_10 = time_now - datetime.timedelta(minutes = 10)
time_now_mins_10 = time_now_mins_10.strftime('%b %d %H:%M')

#  get time - 60 mins in same format as /var/log/messages
time_now_mins_60 = time_now - datetime.timedelta(minutes = 60)
time_now_mins_60 = time_now_mins_60.strftime('%b %d %H:%M')


def check_count(counter):
        print "Total Number of occurences in 10 mins: %s" % (counter)
        return counter


def check_10min_occurences(get_logger_entry, time_now_mins_10):
        search_file = False
        with open("/var/log/monit/service.log", "r") as inFile:
                count = 0
                for line in inFile:
                        line = line.strip()
                        if search_file:             # check every entry since date and time match
                                if get_logger_entry in line:  # check to see if the line matches a monit restart
                                        count += 1            # if it matches, add 1 to the counter
                        elif time_now_mins_10 in line:  # check 10 mins worth of logs via the time stamp
                                 search_file = True    # start checking the the logs once the time stampt is matched
        return count


curl_response = subprocess.call(["curl --output /dev/null --silent --head --fail -k --connect-timeout 30 https://localhost -H 'Host: test.lazyluke.xyz'"], shell=True)
get_logger_entry = "Service was restarted on"

if curl_response > 0:  # eg NOT 200 OK
        log_count = check_10min_occurences(get_logger_entry, time_now_mins_10)
        if log_count < 3:  # check to see if monit has restarted the service more than 3 times in the last 10 mins
                print "Site down"
                subprocess.call(["sudo -u user -H sh -c 'sudo /bin/systemctl restart httpd' "], shell=True)
                subprocess.call(["/usr/bin/logger -s 'MONIT: Service was restarted on ' `date` 2>>/var/log/monit/service.log"], shell=True)  # add a log entry for the restart
        elif log_count >= 3:
                subprocess.call(["/usr/bin/logger -s 'Monit: Service has been restarted more then 3 times in 10 mins - NO action taken' 2>>/var/log/monit/service.log"], shell=True)  # add a log entry for the restart
        else:
                print "Site is Online: no need to restart service"
