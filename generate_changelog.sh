#!/bin/bash

# Set the default time period (optional)
TIME_PERIOD=2

# Check if a command-line argument is provided for time period
if [ $# -gt 0 ]; then
    TIME_PERIOD=$1
fi

# Run the Python script with the specified time period
python3 generate_changelog.py --time_period "$TIME_PERIOD"
