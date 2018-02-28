#!/bin/sh 

# Simple wrapper script, allows us to set exit codes and manipulate json output. 
# TODO: parse the json output and add some kind of .ignore file so
# that we can filter out false positives, may rewrite this in python.

# Check if --json param is set, if so we'll pipe the output via jq
for i in "$@" ; do
  if [[ $i == "--json" ]]; then
    json=true
    break
  fi
done

if [[ $json ]]; then
  output="$(trufflehog --regex --rules /trufflehog/regex.rules.json file:///git "$@" | jq -C .)"
else
  output="$(trufflehog --regex --rules /trufflehog/regex.rules.json file:///git "$@")"
fi

if [ "${output}" != "" ]; then
  echo "${output}"
  exit 1
else
  exit 0
fi
