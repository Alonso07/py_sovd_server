#!/bin/bash
# Resolve symlinks in src/sovd_server so Poetry can build a wheel (it cannot include
# files outside src/ when symlinks point to generated/). Run from repo root.
# Usage: ./scripts/build_resolve_symlinks.sh [install|build|restore]
#   install: copy generated code over symlinks (so tree is real files)
#   restore: restore symlinks (git checkout)
#   build:   install, poetry build, restore

set -e
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"
PKG="$REPO_ROOT/src/sovd_server"
GEN="$REPO_ROOT/generated/sovd_server"

install_content() {
  echo "Resolving symlinks for build..."
  for name in controllers models encoder.py typing_utils.py util.py; do
    if [ -L "$PKG/$name" ]; then
      rm "$PKG/$name"
      cp -R "$GEN/$name" "$PKG/$name"
    fi
  done
}

restore_symlinks() {
  echo "Restoring symlinks..."
  git checkout -- src/sovd_server/controllers src/sovd_server/models \
    src/sovd_server/encoder.py src/sovd_server/typing_utils.py src/sovd_server/util.py 2>/dev/null || true
}

case "${1:-build}" in
  install)  install_content ;;
  restore)  restore_symlinks ;;
  build)
    install_content
    poetry build
    restore_symlinks
    ;;
  *) echo "Usage: $0 [install|restore|build]"; exit 1 ;;
esac
