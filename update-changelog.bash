#!/bin/bash
#
# Automate the process of updating the CHANGELOG.md file, based on the latest commit
# messages from the dotfiles submodule.
#
# Version: v1.1.3
# License: MIT License
#          Copyright (c) 2024-2025 Hunter T. (StrangeRanger)
#
########################################################################################
####[ Global Variables ]################################################################


readonly C_REF_BRANCH="origin/main"
readonly C_CHANGELOG="CHANGELOG.md"
readonly C_TMP_CHANGELOG="CHANGELOG.tmp"
readonly C_SUBMODULE_PATH="submodules/dotfiles"

C_REF_BRANCH_COMMIT=$(git rev-parse "$C_REF_BRANCH":submodules/dotfiles)
C_DATE=$(date +%Y-%m-%d)
readonly C_REF_BRANCH_COMMIT C_DATE

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


echo "${C_INFO}Initializing submodule..."
git submodule update --init "$C_SUBMODULE_PATH"

###
### Checkout the latest commit of the submodule 'dotfiles' in the reference branch.
###

echo "${C_INFO}Checking out the latest commit of the submodule 'dotfiles' in the" \
    "reference branch..."

git -C "$C_SUBMODULE_PATH" checkout "$C_REF_BRANCH_COMMIT"

###
### Extract latest commit messages.
###

echo "${C_INFO}Updating the submodule..."
git submodule update --remote "$C_SUBMODULE_PATH"

cd "$C_SUBMODULE_PATH" || {
    echo "${C_ERROR}Failed to change directory to the dotfiles submodule"
    exit 1
}

echo "${C_INFO}Fetching latest commits in current branch..."
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
    if [[ $commit =~ ^(added|changed|removed|fixed|other)(\([^\)]*\))?:\ (.+)$ ]]; then
        type="${BASH_REMATCH[1]^}"
        info="${BASH_REMATCH[2]}"
        message="${BASH_REMATCH[3]}"

        ## Debugging output.
        echo "Type: $type"
        echo "Info: $info"
        echo "Message: $message"

        ## Skip commits that only affect the dotfiles repository.
        if [[ $info == "(chezmoi)" || $info == "(dotfiles)" ]]; then
            skip=true
        fi
    else
        echo "Commit Message: '$commit'"
        skip=true
    fi

    if [[ $skip == true ]]; then
        echo "Add to CHANGELOG: false"
        echo "---"  # Debug separator.
        continue
    fi

    echo "Add to CHANGELOG: true"
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

## NOTE: The function is necessary, as 'awk -v' on macOS doesn't support values with literal
##  newline characters.
awk -v new_entry_file="$C_TMP_CHANGELOG" '
    function emit_file(path,    line) {
        while ((getline line < path) > 0) print line
        close(path)
    }

    /^## Unreleased$/ {
        print
        print ""
        emit_file(new_entry_file)
        next
    }
    { print }
' "$C_CHANGELOG" > "${C_CHANGELOG}.tmp"

mv "${C_CHANGELOG}.tmp" "$C_CHANGELOG"

echo "${C_INFO}Cleaning up..."
rm "$C_TMP_CHANGELOG"

