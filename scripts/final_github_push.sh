#!/bin/bash
# 🚀 Boofa-Med Final GitHub Push Script
set -e
echo '🩺 Boofa-Med: GitHub Launch Sequence'
git add .
git commit -m 'feat: final Boofa-Med submission bundle' || echo 'No changes'
git push origin main --force
echo '✅ SUCCESS: Boofa-Med is live on GitHub!'
