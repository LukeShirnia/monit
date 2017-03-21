# monit
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
 
 Now use the python script located in this repository as the "exec" part of the monit logic.
 <br />
 
The python script runs a bash curl command (yes, its not ideal to run a bash command). 
<br />
Replace `https://localhost -H 'Host: test.lazyluke.xyz'` in the following curl command in the python script with the application/website you wish to monitor

 
`curl_response = subprocess.call(["curl --output /dev/null --silent --head --fail -k --connect-timeout 30 https://localhost -H 'Host: test.lazyluke.xyz'"], shell=True)`
