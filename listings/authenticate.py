from rest_framework.authentication import SessionAuthentication

class SessionCsrfExemptAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass



class CsrfExempt(SessionAuthentication):
    def enforce_csrf(self, request):
        pass

