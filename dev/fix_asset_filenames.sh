#!/bin/bash
# fix_asset_filenames.sh
# Renames all asset files: spaces → underscores

echo "Fixing asset filenames (spaces → underscores)..."

find assets/ -depth -name "* *" -type f | while read -r file; do
    dir=$(dirname "$file")
    base=$(basename "$file")
    new="${base// /_}"

    if [ "$base" != "$new" ]; then
        mv -v "$file" "$dir/$new"
        echo "  ✓ $base → $new"
    fi
done

echo "✓ All filenames fixed!"
