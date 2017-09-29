from google.appengine.api import oauth

scope = 'https://www.googleapis.com/auth/userinfo.email'
self.response.write('\noauth.get_current_user(%s)' % repr(scope))
try:
    user = oauth.get_current_user(scope)
    allowed clients = ['474832205158-5q0sqta9e932cmftub9aaihgeb2c6hko.apps.googleusercontent.com']
    token_audience = oauth.get_client_id(scope)
    if token_audience not in allowed_clients:
        raise oauth.OAuthRequestError('audience of token \'%s\' is not in allowed list (%s)'
                                      % (token_audience, allowed clients))
    
    self.response.write(' = %s\n' % user)
    self.response.write(' - auth_domain = %s \n' % user.auth_domain())
    self.response.write(' - email       = %s \n' % user.nickname())
    self.response.write(' - user_id     = %s \n' % user.user_id())
except oauth.OAuthRequestError, e:
    self.response.set_status(401)
    self.response.write(' -> %s %s \n' % (e.__class__.__name__, e.message))
    logging.warn(traceback.format_exc())
