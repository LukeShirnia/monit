# monit
A basic python script used to check the responsiveness of a local application/website. Executing the python script using monit
<br />

### Example Monit Configuration:

```
check host localhost with address localhost every 2 cycles
   if failed
       port 443 protocol https
       with http headers [Host: test.lazyluke.xyz, Cache-Control: no-cache]
       and request /
    then exec "/home/python/monit_service_check.py"
```
 <br />
 
 Now use the python script located in this repository as the "exec" part of the monit logic
