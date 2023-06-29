from django.http import HttpResponseServerError, HttpResponseNotFound, Http404

# catches exceptions raised during the request/response cycle and handles them accordingly.
# If the exception is an Http404 (Page Not Found), it returns a 404 response.
# For other exceptions, it returns a 500 response.
#
# To enable the global exception handling, you need to add the handler500 or handler404
# view to your urls.py file or include the custom middleware in your middleware settings.

# Global Exception Handler
class GlobalExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        # If no response, raise status methods
        except Exception as e:
            if isinstance(e, Http404):
                return HttpResponseNotFound("Page not found")
            else:
                return HttpResponseServerError("Internal Server Error")
        return response


# When using the handler500 decorator or middleware, Django will automatically use them for
# any unhandled exceptions that occur during the request processing. Similarly, the handler404
# decorator or middleware will be used for 404 errors.