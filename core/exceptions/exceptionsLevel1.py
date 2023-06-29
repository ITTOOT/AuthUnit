#  define your own exception classes by subclassing Django's
#  Exception class or any other relevant built-in exception class.

# Custom Exception
class CustomException(Exception):
    pass

class SpecificException(CustomException):
    pass

class SpecificException2(CustomException):
    pass

# Usage
# try:
#     perform_action()
# except SpecificException as e:
#     # Handle the specific exception
#     print(f"Specific exception occurred: {e}")
# except CustomException as e:
#     # Handle the base custom exception
#     print(f"Custom exception occurred: {e}")
# except Exception as e:
#     # Handle other exceptions
#     print(f"Unhandled exception occurred: {e}")