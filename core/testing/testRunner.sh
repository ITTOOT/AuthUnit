#!/bin/bash

# Grant executable permissions to the shell script:
# chmod +x test_runner.sh

# Run the shell script:
# ./test_runner.sh

# Set the path to the script and the directory to monitor
SCRIPT_PATH="/core/testing/testRunner.py"
DIRECTORY_TO_MONITOR="/AuthorizationUnit"

# Start the monitoring
echo "Monitoring directory: $DIRECTORY_TO_MONITOR"
echo "Press Ctrl+C to stop"
echo ""

while true
do
    python $SCRIPT_PATH

    # Wait for changes in the directory
    echo ""
    echo "Waiting for changes..."
    echo ""

    # Use the `watchmedo` command to monitor the directory for changes
    watchmedo auto-restart --patterns="*.py" --recursive --directory=$DIRECTORY_TO_MONITOR --command="python $SCRIPT_PATH"
done

# Now, whenever a change is made to any Python file within the monitored directory,
# the test_runner.py script will be executed automatically. The test results will
# be saved in the specified log file.