# DNS Propagation Checker API
This is a simple API to get the DNS Propagation


### Install virtualenv
```
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org virtualenv
```
### Initilise
```
virtualenv -p /usr/bin/python apienv
```
### Active
```
source apienv/bin/activate
```
### Install
```
pip install -r req.txt
```

### Start app
```
python api/app.py
```

### Deactivate
```
deactivate
```

### Usage
```
curl --location --request POST 'http://localhost:8000/dns-propagation-checker' \
--header 'Content-Type: application/json' \
--data-raw '{
       "FQDN" : "google.com",
       "DNS_Record" : "A"
}'

```
Vault
https://modularsystems.io/blog/securing-secrets-python-vault/
