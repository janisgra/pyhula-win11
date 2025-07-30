# pyhula-win11


## Submodules

We pull in [pyhula-install-wrapper](https://github.com/janisgra/pyhula-install-wrapper.git) as a Git submodule under `submoduls/` so its code stays separate and easy to update.

### 1. Adding the Submodule

Run this once (or skip if it’s already there):

```bash

git config -f .gitmodules submodule.submoduls/pyhula-install-wrapper.branch master
git add .gitmodules submoduls/pyhula-install-wrapper
git commit -m "Add pyhula-install-wrapper submodule"
```

### 2. Cloning the Repo (with Submodules)

After you git clone the main repo, initialize and fetch submodules in one go:
```bash
git submodule update --init --recursive
```

### 3. Pulling In Upstream Updates

Whenever `pyhula-install-wrapper` sees new commits, run:
```bash
git submodule update --remote --merge
git add submoduls/pyhula-install-wrapper
git commit -m "Update pyhula-install-wrapper to latest"
```

*Optional:* set an alias in your `~/.gitconfig` for one-liner updates:

```ini
[alias]
  smu = "!git submodule update --init --remote --merge && git add . && git commit -m 'Update submodules'"
```

