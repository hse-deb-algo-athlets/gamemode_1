#!/bin/bash

# Check if correct number of arguments provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 source_repo_url destination_repo_url"
    exit 1
fi

SOURCE_REPO=$1
DEST_REPO=$2

# Get the repository name from the source repository URL
REPO_NAME=$(basename -s .git "$SOURCE_REPO")

# Clone the source repository
git clone "$SOURCE_REPO" "$REPO_NAME-clean"

cd "$REPO_NAME-clean" || exit 1

# Remove files and folders matching "*solution*" from the entire git history
git filter-branch --force --index-filter \
    'git rm -r --cached --ignore-unmatch "*solution*"' \
    --prune-empty --tag-name-filter cat -- --all

# Clean up unnecessary files and optimize the repository
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now

# Set the destination repository as the new origin
git remote remove origin
git remote add origin "$DEST_REPO"

# Push the cleaned repository to the destination
git push -u origin --all
git push -u origin --tags

echo "Repository forked to $DEST_REPO without files and folders matching '*solution*'."
