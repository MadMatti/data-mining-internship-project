import msal

def connect(authority, client_id, scope, secret):
    
    app = msal.ConfidentialClientApplication(client_id, client_credential=secret, authority=authority)
    result = app.acquire_token_silent(scope, account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=scope)
    return result['access_token']
