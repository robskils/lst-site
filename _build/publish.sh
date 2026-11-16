#!/usr/bin/env bash
# Pull anything the CRM has written and commit the pages.
#
# All the thinking lives here rather than in the workflow file, so the
# workflow itself stays short enough to be created in one go in the GitHub
# editor without anything getting lost in a paste.
set -euo pipefail

python3 _build/pull_posts.py

if [ -z "$(git status --porcelain)" ]; then
  echo "Nothing new to publish."
  exit 0
fi

git config user.name  "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git add blog
NEW=$(git diff --cached --name-only --diff-filter=A -- 'blog/*/index.html' | wc -l | tr -d ' ')
git commit -m "Publish ${NEW} blog post(s) from the queue"
git push
