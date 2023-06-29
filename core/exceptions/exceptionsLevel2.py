#  define your own exception classes by subclassing Django's
#  Exception class or any other relevant built-in exception class.

# Custom Exception
class CustomException(Exception):
    pass

class SpecificException(CustomException):
    pass

class SpecificException2(CustomException):
    pass