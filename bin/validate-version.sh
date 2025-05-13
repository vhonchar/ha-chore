#!/bin/bash

set -e

TAG=$(./bin/version.sh)

echo "🔍 Checking version: $TAG"

if ! [[ "$TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "❌ Version '$TAG' is not valid semantic version (expected format X.Y.Z)"
  exit 1
fi

if git ls-remote --tags origin | grep -q "refs/tags/$TAG$"; then
  echo "❌ Tag $TAG already exists in GitHub"
  exit 1
else
  echo "✅ Tag $TAG does not exist yet — safe to release"
fi
