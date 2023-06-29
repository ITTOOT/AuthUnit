from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.testing.frontend.seleniumUtilities import perform_login


# 1
# Select browser type
selected_browser = "chrome"  # Replace with the browser selected from the frontend

# Login
driver = perform_login(selected_browser)

# Open the login page
driver.get('http://localhost:8000/login')

# Find the username and password fields and enter credentials
username_field = driver.find_element(By.CSS_SELECTOR, '[name="username"]')
password_field = driver.find_element(By.CSS_SELECTOR, '[name="password"]')
username_field.send_keys('your_username')
password_field.send_keys('your_password')

# Submit the form
password_field.send_keys(Keys.RETURN)

# Wait for the page to load after login
wait = WebDriverWait(driver, 10)
welcome_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.welcome-message')))

# Perform assertions or further actions on the logged-in page
assert welcome_message.text == 'Welcome, your_username!'

# Close the WebDriver
driver.quit()


# 2
# Select browser type
selected_browser = "chrome"  # Replace with the browser selected from the frontend

# Login
driver = perform_login(selected_browser)

# Perform the necessary steps to navigate to the change email page

# Find the email input field and update the value
email_field = driver.find_element(By.CSS_SELECTOR, '[name="email"]')
email_field.clear()
email_field.send_keys('example@example.com')

# Perform assertions or further actions

# Close the WebDriver
driver.quit()


# 3
# Select browser type
selected_browser = "chrome"  # Replace with the browser selected from the frontend

# Login
driver = perform_login(selected_browser)

# Perform the necessary steps to navigate to the form page

# Find the form input fields and enter values
input_field1 = driver.find_element(By.CSS_SELECTOR, '[name="input1"]')
input_field2 = driver.find_element(By.CSS_SELECTOR, '[name="input2"]')
input_field1.send_keys('value1')
input_field2.send_keys('value2')

# Submit the form
submit_button = driver.find_element(By.CSS_SELECTOR, '.submit-button')
submit_button.click()

# Perform assertions or further actions

# Close the WebDriver
driver.quit()


# 4
# Select browser type
selected_browser = "chrome"  # Replace with the browser selected from the frontend

# Login
driver = perform_login(selected_browser)

# Perform the necessary steps to navigate to the logout page

# Find the logout button and click it
logout_button = driver.find_element(By.CSS_SELECTOR, '.logout-button')
logout_button.click()

# Perform assertions or further actions

# Close the WebDriver
driver.quit()


# 5
# Select browser type
selected_browser = "chrome"  # Replace with the browser selected from the frontend

# Login
driver = perform_login(selected_browser)

# Perform the necessary steps to navigate to a restricted page

# Perform assertions or further actions to verify the access restriction message or behavior

# Close the WebDriver
driver.quit()



