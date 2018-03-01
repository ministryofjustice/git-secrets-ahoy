# git-secrets-ahoy
Implementation of truffleHog in docker image with git hooks scripts

## How to use:

The docker image allows easy execution of truffleHog against a chosen git repo.  Note: the docker image expects to find your repo mounted inside the image at */git*, see `-v` option in examples.

First...
```
cd your_git_repo
```
```
docker pull mojdigitalstudio/git-secrets-ahoy
```

## Examples

To scan the entire commit history of your repo:
```
docker run -t --rm -v "$PWD:/git" mojdigitalstudio/git-secrets-ahoy
```

To scan the last commit, provide the `--since_commit` option with the commit hash of where to start scanning: e.g.
```
docker run -t --rm -v "$PWD:/git" mojdigitalstudio/git-secrets-ahoy --use_current_branch --since_commit $(git rev-parse HEAD~1)
```

Output in json:
```
docker run -t --rm -v "$PWD:/git" mojdigitalstudio/git-secrets-ahoy --json
```

## Install Git Hooks

Run the `install_hooks.sh` helper script in the root of your repo.
```
bash <(curl -fsSL https://raw.githubusercontent.com/ministryofjustice/git-secrets-ahoy/master/install_hooks.sh)
```

### post-commit
Just displays a warning if you commit something potentially sensitive.  You can optionally revert your commit at this stage e.g. before you push it to a public repo.

### pre-push
If truffleHog finds potentially sensitive data in your commits, the hook will abort the push.  You have the option to disregard and push again with the `--no-verify` option, which will skip the pre-push hook.


