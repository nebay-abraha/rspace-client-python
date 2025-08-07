#!/bin/bash

set -euo pipefail

# Ensure jq is installed
if ! command -v jq &> /dev/null; then
  echo "jq not found, installing..."
  sudo apt-get update && sudo apt-get install -y jq
fi

# Fetch latest release version
echo "Fetching latest RSpace release version..."
latest_version=$(curl -s https://api.github.com/repos/rspace-os/rspace-web/releases | jq -r '.[0].name')

if [[ -z "$latest_version" ]]; then
  echo "Error: Could not determine latest version."
  exit 1
fi

echo "Latest RSpace version: $latest_version"

# Download WAR file into current working directory (assumed to be rspace-docker)
war_file="researchspace-${latest_version}.war"
target_path="rspace.war"
download_url="https://github.com/rspace-os/rspace-web/releases/download/${latest_version}/${war_file}"

echo "Downloading WAR from: $download_url"
curl -L "$download_url" -o "$target_path"

echo "WAR downloaded as: $target_path"
