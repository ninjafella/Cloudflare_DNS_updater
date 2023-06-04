# Cloudflare_DNS_updater

## <u>Logging</u>
```python
LOGS : bool = True | False
```
This signals whether you wish to have the logs saved to a file (True) or just printed out to the console.

```python
LOGS_FILE : str = 'CloudflareDNS.log'
```
The path for the log file.

```python
LOGGING_LEVEL : int = logging.DEBUG
```
The level at which logging will be recorded. Can be set to: 
- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL
---
## <u>Main config</u>
```python
IP_FILE : str = 'ipaddr.txt'
```
Filepath to save the current IP address to.
```python
DOMAIN : str = '<example.com>'
```
The domain to update.
```python
PROXIED : bool = True
```
Whether the DNS record is proxied through Cloudflare or not.
```python
CF_EMAIL : str = 'john@<example>.com' 
```
Email address used to login to Cloudflare.
```python
CF_API_KEY : str = '<API key>'
```
Global API key from Cloudflare.
```python
ZONE_ID : str = '<Zone ID>'
```
Zone ID from Cloudflare.
```python
RECORD_ID : Union[str, list] = '<record ID>'
```
This has two different settings. It can either be set to a single string or a list of strings for multiple records to be changed.
<br>
If a single string is used it will update the it as if it is for the root domain. If a list is used then the domains will be set in a specific order:

1. Will be for the root domain
2. Will be for subdomains
2. Will be for the www subdomain

Not all 3 need to be filled in. It will work just fine with the first 2.


Have fun. Feel free to provide improvements and report and errors that you are having with this.