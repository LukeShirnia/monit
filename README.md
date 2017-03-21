# monit

Note: ONLY WORKS WITH CENTOS AND RHEL



A basic python script used to check the responsiveness of a local application/website. 
<br />

This uses a combination of monit and python to prevent a continuous loop of restarting the service
<br />

<br />


### Example Monit Configuration:
Apply the following configuration to `/etc/monit.d/filename`
```
check host localhost with address localhost every 2 cycles
   if failed
       port 443 protocol https
       with http headers [Host: test.lazyluke.xyz, Cache-Control: no-cache]
       and request /
    then exec "/home/python/monit_service_check.py"
```
 <br />
 
<br />
 

### monit_service_check Python Script
 Now use the python script located in this repository as the "exec" part of the monit logic.
<br />

### Replace
##### Replace Part 1 )
The python script will attempt to write to `/var/log/monit/service.log`. Find and replace all instance of this path in the file (EXCEPT `open("/var/log/messages")`) with a filename of your choosing and make sure the directory and file exist. 
<br />

<br />


##### Replace Part 2 )
The python script runs a bash curl command (yes, its not ideal to run a bash command). 
<br />


Replace `https://localhost -H 'Host: test.lazyluke.xyz'` in the following curl command in the python script with the application/website you wish to monitor
<br />


 
```
curl_response = subprocess.call(["curl --output /dev/null --silent --head --fail -k --connect-timeout 30 https://localhost -H 'Host: test.lazyluke.xyz'"], shell=True)
```
