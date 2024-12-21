#!/bin/bash
#
# Automate the process of updating the CHANGELOG.md file, based on the latest commit
# messages from the dotfiles submodule.
#
# Version: v1.0.0
# License: MIT License
#          Copyright (c) 2024 Hunter T. (StrangeRanger)
#
########################################################################################
####[ Global Variables ]################################################################


readonly C_CHANGELOG="CHANGELOG.md"
readonly C_TMP_CHANGELOG="CHANGELOG.tmp"
readonly C_SUBMODULE_PATH="submodules/dotfiles"

C_DATE=$(date +%Y-%m-%d)
readonly C_DATE

## ANSI color codes.
C_BLUE="$(printf '\033[0;34m')"
C_RED="$(printf '\033[1;31m')"
C_NC="$(printf '\033[0m')"
readonly C_BLUE C_RED C_NC

## Shorthanded variables for colorized output.
readonly C_ERROR="${C_RED}ERROR:${C_NC} "
readonly C_INFO="${C_BLUE}==>${C_NC} "

declare -A sections


####[ Main ]############################################################################


###
### Extract latest commit messages.
###

echo "${C_INFO}Updating submodule..."
git submodule update --remote

cd "$C_SUBMODULE_PATH" || {
    echo "${C_ERROR}Failed to change directory to '$C_SUBMODULE_PATH'"
    exit 1
}

echo "${C_INFO}Fetching latest commits..."
C_COMMITS=$(git log "$(git rev-parse HEAD@"{1}")..HEAD" --pretty=format:"%s")

if [[ -z $C_COMMITS ]]; then
    echo "${C_ERROR}Could not determine previous commit(s)"
    exit 1
fi

cd - || {
    echo "${C_ERROR}Failed to change directory back to project's root directory"
    exit 1
}

echo "${C_INFO}Prepping new changelog entry..."
{
    echo "## $C_DATE"
    echo ""
} > "$C_TMP_CHANGELOG"

###
### Parse commit messages and append to the appropriate section.
###

echo "${C_INFO}Parsing commit messages..."

while IFS= read -r commit; do
    skip=false

    # Regex to capture type, optional info, and optional message.
    if [[ $commit =~ ^(added|changed|removed|fixed)(\([^\)]*\))?:\ (.+)$ ]]; then
        type="${BASH_REMATCH[1]^}"
        info="${BASH_REMATCH[2]}"
        message="${BASH_REMATCH[3]}"

        ## Debugging output.
        echo "Type: $type"
        echo "Info: $info"
        echo "Message: $message"

        ## Skip commits that only affect the dotfiles repository.
        if [[ "$info" == "(chezmoi)" || "$info" == "(dotfiles)" ]]; then
            skip=true
        fi
    fi

    if [ "$skip" = true ]; then
        echo "---"  # Debug separator.
        continue
    fi

    # Append commit to the appropriate section.
    sections["$type"]+="- $commit"$'\n'
    echo "---"  # Debug separator.
done <<< "$C_COMMITS"

###
### Add new entries to the changelog.
###

echo "${C_INFO}Updating the changelog..."
for type in "${!sections[@]}"; do
    {
        echo "### $type"
        echo ""
        echo "${sections[$type]}"
    } >> "$C_TMP_CHANGELOG"
done

awk -v new_entry="$(cat $C_TMP_CHANGELOG)" '
   /^## Unreleased$/ {
       print;
       print "";
       print new_entry;
       next
   }
   { print }
' "$C_CHANGELOG" > "${C_CHANGELOG}.tmp"

mv "${C_CHANGELOG}.tmp" "$C_CHANGELOG"

echo "${C_INFO}Cleaning up..."
rm "$C_TMP_CHANGELOG"
