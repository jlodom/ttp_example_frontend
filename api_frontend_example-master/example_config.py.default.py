import requests

# Variables defined for all routines
clientsecret = 'SOMEOAUTHSECRET'
clientid = 'SOMEOAUTHCLIENTID'
# The following  four variables are for ECSD config.
# I decided they were not as sensitive as other stuff.
oauthurl = 'https://accessmanager.nothing.com' # Access Manager OAuth URL
localurl = 'http://127.0.0.1:5002' # URL where this application is running from
apiurl = 'https://127.0.0.1:5000' # URL where the back-end API is running
scopewanted = 'someoauthscope'
resourceServer = 'someauthresourceserver' # NOT a server name, the name of an Access Manager Resource Server
nonce = 'ab8932b6'
state = 'AB32623HS'

def NamRetrieveToken(code):
    r = requests.post(oauthurl + '/nidp/oauth/nam/token', verify=False, data={'client_id': clientid, 'client_secret': clientsecret,
                                                   'code': code, 'resourceServer': resourceServer, 'grant_type': 'authorization_code', 'redirect_uri': localurl + '/'})
    return r.json()