#!/bin/bash

set -e

MANIFEST_PATH="custom_components/chore/manifest.json"

if ! [ -f "$MANIFEST_PATH" ]; then
  echo "❌ Manifest file not found: $MANIFEST_PATH"
  exit 1
fi

VERSION=$(jq -r '.version' "$MANIFEST_PATH")

echo "v$VERSION"