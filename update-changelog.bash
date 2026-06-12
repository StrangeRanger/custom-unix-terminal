#!/bin/bash
#
# Automate the process of updating the CHANGELOG.md file, based on the latest commit
# messages from the dotfiles submodule.
#
# NOTE: This script was rewritten with Codex and modified by Hunter T.
#
# Version: v2.0.0
# License: MIT License
#          Copyright (c) 2024-2026 Hunter T. (StrangeRanger)
#
############################################################################################
set -euo pipefail
####[ Global Variables ]####################################################################


readonly C_REF_BRANCH="origin/main"
readonly C_CHANGELOG="CHANGELOG.md"
readonly C_SUBMODULE_PATH="submodules/dotfiles"

C_REF_BRANCH_COMMIT=$(git rev-parse "$C_REF_BRANCH:$C_SUBMODULE_PATH")
C_DATE=$(date +%Y-%m-%d)
readonly C_REF_BRANCH_COMMIT C_DATE

# Write the complete replacement changelog to a temp file before replacing the original.
C_TMP_UPDATED_CHANGELOG=$(mktemp "${TMPDIR:-/tmp}/update-changelog.XXXXXX")
readonly C_TMP_UPDATED_CHANGELOG

readonly C_BLUE=$'\033[0;34m'
readonly C_NC=$'\033[0m'

readonly C_INFO="${C_BLUE}==>${C_NC} "

added_entries=""
changed_entries=""
fixed_entries=""
removed_entries=""
other_entries=""
has_entries=false
wrote_section=false


####[ Functions ]###########################################################################


####
# Append a commit message to the appropriate section based on its type.
#
# MODIFIED GLOBALS:
#   - added_entries, changed_entries, fixed_entries, removed_entries, other_entries
#   - has_entries: Indicates whether any entries have been added.
append_entry() {
    local type=$1
    local commit=$2

    case "$type" in
        added)
            added_entries+="- $commit"$'\n'
            ;;
        changed)
            changed_entries+="- $commit"$'\n'
            ;;
        fixed)
            fixed_entries+="- $commit"$'\n'
            ;;
        removed)
            removed_entries+="- $commit"$'\n'
            ;;
        other)
            other_entries+="- $commit"$'\n'
            ;;
    esac

    has_entries=true
}

####
# Write one Markdown section to stdout when that section has entries.
#
# MODIFIED GLOBALS:
#   - wrote_section: Set to true if a section was emitted, which is used to determine
#     whether to print a blank line before the next section.
emit_section() {
    local title=$1
    local entries=$2

    [[ -n $entries ]] || return 0

    if [[ $wrote_section == true ]]; then
        printf '\n'
    fi

    printf '### %s\n\n' "$title"
    printf '%s' "$entries"
    wrote_section=true
}


####[ Trapping Logic ]######################################################################


trap 'rm -f "$C_TMP_UPDATED_CHANGELOG" || true' EXIT


####[ Main ]################################################################################


echo "${C_INFO}Initializing submodule..."
git submodule update --init "$C_SUBMODULE_PATH"

echo "${C_INFO}Checking out the latest commit of the submodule 'dotfiles'"
git -C "$C_SUBMODULE_PATH" checkout --quiet "$C_REF_BRANCH_COMMIT"

###
### Extract latest commit messages.
###

echo "${C_INFO}Updating the submodule..."
git submodule update --remote "$C_SUBMODULE_PATH"

echo "${C_INFO}Fetching latest commits in current branch..."
C_COMMITS=$(git -C "$C_SUBMODULE_PATH" log "$C_REF_BRANCH_COMMIT..HEAD" --pretty=format:"%s")

if [[ -z $C_COMMITS ]]; then
    echo "${C_INFO}No new commits found; leaving $C_CHANGELOG unchanged."
    exit 0
fi

###
### Parse commit messages and append to the appropriate section.
###

echo "${C_INFO}Parsing commit messages..."

while IFS= read -r commit; do
    if [[ $commit =~ ^(added|changed|removed|fixed|other)(\([^\)]*\))?:[[:space:]]+(.+)$ ]];
    then
        type="${BASH_REMATCH[1]}"
    else
        continue
    fi

    append_entry "$type" "$commit"
done <<< "$C_COMMITS"

if [[ $has_entries == false ]]; then
    echo "${C_INFO}No changelog entries found; leaving $C_CHANGELOG unchanged."
    exit 0
fi

###
### Add new entries to the changelog.
###

echo "${C_INFO}Updating the changelog..."

inserted=false
skip_blank_after_entry=false
line=""

# Rewrite the changelog line by line, inserting the new dated entry under Unreleased.
# The final condition preserves a last line even if the file has no trailing newline.
while IFS= read -r line || [[ -n $line ]]; do
    if [[ $line == "## Unreleased" ]]; then
        printf '%s\n\n' "$line"
        printf '## %s\n\n' "$C_DATE"
        emit_section "Added" "$added_entries"
        emit_section "Changed" "$changed_entries"
        emit_section "Fixed" "$fixed_entries"
        emit_section "Removed" "$removed_entries"
        emit_section "Other" "$other_entries"

        inserted=true
        # Existing blank lines after Unreleased are skipped below and replaced with one.
        skip_blank_after_entry=true
        continue
    fi

    # Drop blank lines immediately after the inserted entry so spacing is deterministic.
    if [[ $skip_blank_after_entry == true && -z $line ]]; then
        continue
    fi

    # Add exactly one blank line before the next existing changelog section.
    if [[ $skip_blank_after_entry == true ]]; then
        printf '\n'
        skip_blank_after_entry=false
    fi

    printf '%s\n' "$line"
done < "$C_CHANGELOG" > "$C_TMP_UPDATED_CHANGELOG"

if [[ $inserted == false ]]; then
    echo "## Unreleased section not found" >&2
    exit 1
fi

mv "$C_TMP_UPDATED_CHANGELOG" "$C_CHANGELOG"
