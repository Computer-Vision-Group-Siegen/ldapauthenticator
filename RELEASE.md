# How to make a release

`ldapauthenticator` is a package [available on PyPI](https://pypi.org/project/jupyterhub-ldapauthenticator/) and
[conda-forge](https://anaconda.org/conda-forge/jupyterhub-ldapauthenticator).
These are instructions on how to make a release on PyPI.
The PyPI release is done automatically by TravisCI when a tag is pushed.

For you to follow along according to these instructions, you need:
- To have push rights to the [ldapauthenticator GitHub
  repository](https://github.com/jupyterhub/ldapauthenticator).

## Steps to make a release

1. Checkout master and make sure it is up to date.

   ```shell
   ORIGIN=${ORIGIN:-origin} # set to the canonical remote, e.g. 'upstream' if 'origin' is not the official repo
   git checkout master
   git fetch $ORIGIN master
   git reset --hard $ORIGIN/master
   # WARNING! This next command deletes any untracked files in the repo
   git clean -xfd
   ```

1. Set the `version` variable in [setup.py](setup.py)
   appropriately and make a commit.

   ```
   git add setup.py
   VERSION=...  # e.g. 1.2.3
   git commit -m "release $VERSION"
   ```

1. Optional: Build local wheel
   To build a local wheel which can be installed with pip, 
   execute the following command:
   ```shell
   python setup.py bdist_wheel
   ```

2. Reset the `version` variable in
   [setup.py](setup.py) appropriately with an incremented
   patch version and a `dev` element, then make a commit.
   ```
   git add setup.py
   git commit -m "back to dev"
   ```

3. Push your two commits to master.

   ```shell
   # first push commits without a tags to ensure the
   # commits comes through, because a tag can otherwise
   # be pushed all alone without company of rejected
   # commits, and we want have our tagged release coupled
   # with a specific commit in master
   git push $ORIGIN master
   ```

4. Create a git tag for the pushed release commit and push it.

   ```shell
   git tag -a $VERSION -m $VERSION HEAD~1

   # then verify you tagged the right commit
   git log

   # then push it
   git push $ORIGIN refs/tags/$VERSION
   ```
