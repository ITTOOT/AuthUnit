import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from core.jwt.jwtMiddleware import getCurrentUser
from core.models.utilityModels import AppSettings


# Retrieve the AppSettings instance from the database
app_settings = AppSettings.objects.first()
web_driver_path = app_settings.webdriver_location
logging_file_path = app_settings.logging_file_location

# Use the retrieved settings in the code
def perform_login(browser):
    # Use the selected browser for the webdriver
    if browser == "chrome":
        driver = webdriver.Chrome(executable_path=web_driver_path)
    elif browser == "edge":
        driver = webdriver.Edge(executable_path=web_driver_path)
    elif browser == "firefox":
        driver = webdriver.Firefox(executable_path=web_driver_path)
    elif browser == "safari":
        driver = webdriver.Safari(executable_path=web_driver_path)
    else:
        raise ValueError("Invalid browser selection")

    logging.basicConfig(filename=logging_file_path, level=logging.INFO)

    return driver

# EXAMPLE
# Example of logging a change
def logUserChange(user, field_name, new_value):
    ip_address = user.ip_address  # Assuming the user model has an 'ip_address' field
    username = user.username

    message = f"Change detected: User '{username}' with IP '{ip_address}' - {field_name} updated to {new_value}"
    logging.info(message)

# Example usage in views/controllers
def changeView(request):
    # Get the user object using getUser function
    user = getCurrentUser(request)

    # Log changes
    field_name = "Email address"
    new_value = "example@example.com"
    logUserChange(user, field_name, new_value)

# Select browser type
selected_browser = "chrome"  # Replace with the browser selected from the frontend

# Login
driver = perform_login(selected_browser)





