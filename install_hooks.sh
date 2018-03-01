#!/bin/bash

hooks_url="https://raw.githubusercontent.com/ministryofjustice/git-secrets-ahoy/master/git_hooks/"
hooks="post-commit pre-push"

docker="$(docker -v)"
if [[ $? -ne 0 ]]; then
  echo "Please install docker, these git hooks require it"
  exit 1
else
  echo "Found docker: ${docker}"
  docker pull mojdigitalstudio/git-secrets-ahoy:latest
fi

if [[ -d ".git/hooks/" ]]; then
  for hook in $hooks; do
    echo "Copying ${hook} hook to .git/hooks/${hook}"
    curl -fsSL "${hooks_url}${hook}" > ".git/hooks/${hook}"
    chmod +x ".git/hooks/${hook}"
  done
else
  echo 'No .git/hooks directory found'
fi
