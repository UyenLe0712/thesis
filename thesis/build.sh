#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
tectonic -X compile main.tex --keep-logs 2>&1 | tail -20 || tectonic main.tex 2>&1 | tail -20
echo "--> thesis/main.pdf"
