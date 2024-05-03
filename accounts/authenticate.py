from rest_framework.authentication import SessionAuthentication

class SessionCsrfExemptAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass


class CsrfExempt(object):
    def enforce_csrf(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)


