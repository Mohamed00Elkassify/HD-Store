from rest_framework.throttling import SimpleRateThrottle


class LoginRateThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}


class CheckoutRateThrottle(SimpleRateThrottle):
    scope = "checkout"

    def get_cache_key(self, request, view):
        # throttle by user if logged in, otherwise IP
        if request.user and request.user.is_authenticated:
            ident = f"user:{request.user.id}"
        else:
            ident = f"ip:{self.get_ident(request)}"
        return self.cache_format % {"scope": self.scope, "ident": ident}
