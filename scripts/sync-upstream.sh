#!/bin/bash
set -e

# Sync FlatCAM upstream (Bitbucket) into local Beta & dev branches

echo "==> Fetching upstream (Bitbucket)..."
git fetch upstream

echo "==> Updating Beta branch..."
git checkout Beta
git merge upstream/Beta --ff-only
git push origin Beta

echo "==> Rebasing dev onto Beta..."
git checkout dev
git rebase Beta
git push origin dev --force-with-lease

echo "==> Done. dev is up-to-date with upstream/Beta."
