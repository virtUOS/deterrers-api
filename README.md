# Python API client for DETERRERS

This library makes it easy to interact with the DETERRERS perimeter firewall
portal to automate registration, and configuration of IP addresses and firewall
profiles.

## Installation

Use pip to install the latest version:

```
pip install deterrers-api
```

## Example

```python
import deterrersapi


deterrers = deterrersapi.Deterrers('https://deterrers.example.com', '<api-token>')

# get information about ip address
deterrers.get('192.0.0.1')

# delete ip address
deterrers.delete('192.0.0.1')

# add a new ip address with `virtUOS` as admin
deterrers.add('192.0.0.1', ['virtUOS'])

# update ip with firewall profile `Multipurpose`
deterrers.update('192.0.0.1', 'Multipurpose', '')

# activate firewall profile
deterrers.action('192.0.0.1', 'register')
```
