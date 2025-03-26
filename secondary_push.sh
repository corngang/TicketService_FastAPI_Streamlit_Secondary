#!/bin/bash

git add --all
git reset .github
git reset manifests
git commit -m "Update files excluding .github and manifests"
git push secondary main