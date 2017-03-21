#!/usr/bin/python
import re
import datetime
import subprocess

# get time
time_now = datetime.datetime.now()

#get time in same format at /var/log/messages
time_now_time = time_now.strftime('%b %d %H:%M')

#get time - 10 mins in same format as /var/log/messages
time_now_mins_10 = time_now - datetime.timedelta(minutes = 10)
time_now_mins_10 = time_now_mins_10.strftime('%b %d %H:%M')

#get time - 60 mins in same format as /var/log/messages
time_now_mins_60 = time_now - datetime.timedelta(minutes = 60)
time_now_mins_60 = time_now_mins_60.strftime('%b %d %H:%M')

def check_count(counter):
        print "Total Number of occurences in 10 mins: %s" % (counter)
        return counter

def check_10min_occurences(get_logger_entry):
        search_file = False
        with open("/var/log/messages", "r") as inFile:
                count = 0
                for line in inFile:
                        line = line.strip()
                        if time_now_mins_10 in line: # check 10 mins worth of logs via the time stamp
                                search_file = True   # start checking the the logs once the time stampt is matched
                        elif search_file:            # check every entry since date and time match
                                if get_logger_entry in line: # check to see if the line matches a monit restart
                                        count += 1           # if it matches, add 1 to the counter
                return count

curl_response = subprocess.call(["curl --output /dev/null --silent --head --fail -k --connect-timeout 30 https://localhost -H 'Host: test.lazyluke.xyz'"], shell=True)
get_logger_entry = "MONIT: Remita Service was restarted on "

if curl_response > 0: # eg NOT 200 OK
        if check_10min_occurences(get_logger_entry) <= 3:  # check to see if monit has restarted the service more than 3 times in the last 10 mins
                print "Site down"
                subprocess.call(["/usr/bin/systemctl restart httpd"] , shell=True)
                subprocess.call(["/usr/bin/logger 'MONIT: Remita Service was restarted on ' `date`"], shell=True), time_now_time # add a log entry for the restart
        elif  check_10min_occurences(get_logger_entry) > 3:
                print "Restarted more than 3 times in the last 10 mins"
        else:
                print "Site is Online: no need to restart service"
