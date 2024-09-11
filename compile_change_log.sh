#!/bin/bash

# Prompt the user for inputs
read -p "Repository owner: " vercel
read -p "Repository name: " next.js
read -p "GitHub token: " token

# Define the API URL
API_URL="http://localhost:3000/commits?owner=$owner&repo=$repo&token=$token"

# Make the API request using curl
response=$(curl -s -X GET "$API_URL")

# Check if the response is empty or contains an error
if [[ -z "$response" ]]; then
    echo "No response from the server. Please ensure the API is running."
    exit 1
fi

# Parse and display the commits
echo "Fetching commits from the last 7 days..."
echo

# Check for errors in the response
error=$(echo "$response" | grep "error")
if [[ -n "$error" ]]; then
    echo "Error: $(echo "$response" | jq -r '.error')"
    exit 1
fi

# Loop through the response and display commit details
commits=$(echo "$response" | jq -r '.[] | "\(.commit.message) by \(.commit.author.name) on \(.commit.author.date)"')

if [[ -z "$commits" ]]; then
    echo "No commits found in the last 7 days."
else
    echo "$commits"
fi
