#!/bin/bash

hooks_url="https://raw.githubusercontent.com/ministryofjustice/git-secrets-ahoy/master/git_hooks/"
hooks="post-commit pre-push"

docker="$(docker -v)"
if [ $? -ne 0 ]; then
  echo "Please install docker, these git hooks require it"
  exit 1
else
  echo "Found docker: ${docker}"
fi

docker pull mojdigitalstudio/git-secrets-ahoy:latest

if [ -d ".git/hooks/"  ]; then
  echo 'copying hooks to .git/hooks/'
  for hook in $hooks; do
    echo "Copying $hook hook"
    curl -fsSL "${hooks_url}${hook}" > ".git/hooks/${hook}"
    chmod +x ".git/hooks/${hook}"
  done
else
  echo 'No .git/hooks directory found'
fi
