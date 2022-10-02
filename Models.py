
class SimpleNote(object):
    def __init__(self, title=None, content=None):
        self.title = title
        self.content = content

    note_id = 0


class SimplenoteCredentials(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

class TokenClaims(object):
    def __init__(self, ver=None, iss=None, sub=None, aud=None, exp=None, iat=None, nbf=None, name=None, perferred_username=None, oid=None, tid=None, aio=None):
        self.ver = ver
        self.iss = iss
        self.sub = sub
        self.aud = aud
        self.exp = exp
        self.iat = iat
        self.nbf = nbf
        self.name = name
        self.preferred_username = perferred_username
        self.oid = oid
        self.tid = tid
        self.aio = aio

class ResponseToken(object):


    def __init__(self, token_type=None, scope=None, expires_in=None, ext_expires_in=None, access_token=None, refresh_token=None, id_token=None, client_info=None, id_token_claims=None):
        self.token_type = token_type
        self.scope = scope
        self.expires_in = expires_in
        self.ext_expires_in = ext_expires_in
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.id_token = id_token
        self.client_info = client_info
        self.id_token_claims = id_token_claims

    token_type = ""
    scope = ""
    expires_in = 0
    ext_expires_in = 0
    access_token = ""
    refresh_token = ""
    id_token = ""
    client_info = ""
    id_token_claims = TokenClaims()

class OneNote(object):
    def __init__(self, title=None, content=None):
        self.title = title
        self.content = content



class Config(object):
    def __init__(self, token=None, secret=None, app_id=None, mode=None, scopes=None, authority_url=None, base_url=None, vendors=None) -> None:
    # def __init__(self, token=None, secret=None, app_id=None, mode=None, scopes=None, authority_url=None, base_url=None) -> None:
        self.token = token
        self.secret = secret
        self.app_id = app_id
        self.mode = mode
        self.scopes = scopes
        self.authority_url = authority_url
        self.base_url = base_url
        self.vendors = vendors

class Vendor(object):
    def __init__(self, username=None, password=None, source_notebook=None, source_section=None) -> None:
        self.username = username
        self.password = password
        self.source_notebook = source_notebook
        self.source_section = source_section