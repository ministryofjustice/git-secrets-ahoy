# git-secrets-ahoy

Re-implementation of [truffleHog](https://github.com/dxa4481/truffleHog) along with some helper scripts for git hooks and CI server use.

## Project Goals

This project began as a wrapper around truffleHog, as we thought it was the most promising tool in the space - the high-entropy feature in particular being a highlight.

After using it for a few days we identified a bunch of small issues, but also ran up against some larger conceptual issues as it seemed to mostly be aimed at doing a point-in-time analysis of an entire repo's history. This led us to strike off on our own.

We aim to meet all of the following goals, many of which are inherited from truffleHog:

* Integrate directly with git repositories
* Checks will be done against a commit or a series of commits
* Primary focus will be high-entropy scanning
* Secondary focus will be regex-based scanning
* Should be easy to run against any git repository
* Allow per-repo configuration via a manifest file that's version controlled
* Provide a way to whitelist secrets or commits that are deemed safe
* Provide a way to exclude files or folders (maybe?)
* Produce human-friendly and/or machine-friendly output
* Support the following scanning scenarios, in descending order of importance:
  1. Use as a local git hook to avoid leaking secrets
  2. Use as a CI task to alert that secrets have been leaked
  3. Use against uncommitted code locally
  4. Use to audit the full history of a repository
* When being used as a CI task:
  * Should be relatively quick, and not increase runtime with length of history
  * Should not stop recording a failure until the commit has been acknowledged or removed (maybe?)

## Installation

### Via Docker Container

The docker image allows easy execution against a chosen git repo.  Note: the docker image expects to find your repo mounted inside the image at */git*, see `-v` option in examples.

```
docker pull mojdigitalstudio/git-secrets-ahoy
```

And then you can run commands using

```
docker run -t --rm -v "$PWD:/git" mojdigitalstudio/git-secrets-ahoy <args>
```

## Usage

```
git-secrets-ahoy [options] [<git-repo>]

options:
  --json                        output in JSON
  --junit-xml                   output in JUnit-style XML
  --no-entropy                  disable high entropy checks
  --entropy-length=<length>     override min word length for entropy check
  --entropy-base64=<limit>      override the threshold for base64 entropy
  --entropy-hex=<limit>         override the threshold for hex entropy
  --no-regex                    disable regex checks
  --no-default-rules            disable default regex rules
  --extra-rules=<rule file>     specify JSON file containing more regex rules
```

### Specifying which commits to scan

Selecting commits to scan is mostly done via the `--revs` or `--one-rev` arguments, which take similar input to the `git log` command. All matching revisions will be scanned.

To scan a single commit
```
--one-rev <commit-hash>
```

To scan a series of commits
```
--revs <commit-from>..<commit-to>
```

To scan the last few weeks of commits
```
--revs master@{2 weeks ago}..HEAD
```

To scan the whole commit history of a branch
```
--revs <commit-hash>
```

To scan staged but uncomitted changes
```
--staged
```

To scan the whole commit history of all branches
```
--all
```

### Installing Git Hooks

Run the `install_hooks.sh` helper script in the root of your repo.
```
bash <(curl -fsSL https://raw.githubusercontent.com/ministryofjustice/git-secrets-ahoy/master/install_hooks.sh)
```

### post-commit
Just displays a warning if you commit something potentially sensitive.  You can optionally revert your commit at this stage e.g. before you push it to a public repo.

### pre-push
If truffleHog finds potentially sensitive data in your commits, the hook will abort the push.  You have the option to disregard and push again with the `--no-verify` option, which will skip the pre-push hook.
