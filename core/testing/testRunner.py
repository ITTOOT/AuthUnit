import os
import sys
import unittest
import datetime
import requests

# Set the path to the project's root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

# Set the path to the test directory
TEST_DIR = os.path.join(PROJECT_ROOT, 'core', 'testing', 'backend')

# Set the path to the log file
LOG_FILE = os.path.join(PROJECT_ROOT, 'core', 'testing', 'backend', 'logs', 'test_logs.txt')

# Set the URL for the alert endpoint
ALERT_URL = 'https://example.com/alerts'

def run_tests():
    # Discover and run the tests
    loader = unittest.TestLoader()
    suite = loader.discover(TEST_DIR)
    runner = unittest.TextTestRunner(stream=sys.stdout)
    result = runner.run(suite)

    # Save the test results to the log file
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'Test results ({timestamp}):\n')
        f.write(f'Errors: {len(result.errors)}\n')
        f.write(f'Failures: {len(result.failures)}\n')
        f.write(f'Skipped: {len(result.skipped)}\n')
        f.write(f'Tests run: {result.testsRun}\n')
        f.write('\n')

    # Send alert if there are errors or failures
    if len(result.errors) > 0 or len(result.failures) > 0:
        alert_message = 'Test failures or errors occurred!'
        send_alert(alert_message)

def send_alert(message):
    payload = {'message': message}
    response = requests.post(ALERT_URL, data=payload)
    if response.status_code == 200:
        print('Alert sent successfully')
    else:
        print(f'Failed to send alert. Status code: {response.status_code}')

if __name__ == '__main__':
    run_tests()
