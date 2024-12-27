#!/bin/bash
#
# Automates the process of setting a custom Gnome Terminal profile as the default.
#
# Version: v1.0.1
# License: MIT License
#          Copyright (c) 2024 Hunter T. (StrangeRanger)
#
########################################################################################
####[ Global Variables ]################################################################


readonly C_PROFILE_FILE_NAME="gnome-terminal-profile.dconf"
readonly C_DCONF_PATH="/org/gnome/terminal/legacy/profiles:/"

# This allows for a more dynamic way to get the UUID of the profile.
C_UUID=$(head -1 "$C_PROFILE_FILE_NAME" | sed 's/^\[:\(.*\)\]/\1/')
readonly C_UUID

## ANSI color codes.
C_YELLOW="$(printf '\033[1;33m')"
C_GREEN="$(printf '\033[0;32m')"
C_BLUE="$(printf '\033[0;34m')"
C_RED="$(printf '\033[1;31m')"
C_NC="$(printf '\033[0m')"
readonly C_YELLOW C_GREEN C_BLUE C_RED C_NC

## Shorthanded variables for colorized output.
readonly C_WARNING="${C_YELLOW}==>${C_NC} "
readonly C_SUCCESS="${C_GREEN}==>${C_NC} "
readonly C_ERROR="${C_RED}ERROR:${C_NC} "
readonly C_INFO="${C_BLUE}==>${C_NC} "


####[ Functions ]#######################################################################


###
### [ Check Functions ]
###

####
# Check if the profile has been loaded into dconf.
#
# RETURNS:
#   - 0: Profile is loaded.
#   - 1: Profile is not loaded.
check_profile_loaded() {
    if dconf list "$C_DCONF_PATH" | grep -q "$C_UUID"; then
        return 0
    else
        return 1
    fi
}

####
# Check if the profile is in the list of profiles.
#
# RETURNS:
#   - 0: Profile is in the list.
#   - 1: Profile is not in the list.
check_profile_in_list() {
    if dconf read "${C_DCONF_PATH}list" | grep -q "$C_UUID"; then
        return 0
    else
        return 1
    fi
}

####
# Check if the profile is the default profile.
#
# RETURNS:
#   - 0: Profile is the default.
#   - 1: Profile is not the default.
check_profile_default() {
    if dconf read "${C_DCONF_PATH}default" | grep -q "$C_UUID"; then
        return 0
    else
        return 1
    fi
}

###
### [ Action Functions ]
###

####
# Load the profile into dconf.
load_profile() {
    echo "${C_INFO}Loading profile..."
    dconf load "$C_DCONF_PATH" < "$C_PROFILE_FILE_NAME"

    echo "${C_INFO}Verifying profile was loaded..."
    if ! check_profile_loaded; then
        echo "${C_ERROR}Profile failed to load"
        exit 1
    fi
}

####
# Add the profile to the list of profiles.
add_profile_to_list() {
    local current_list
    local updated_list

    current_list=$(dconf read "${C_DCONF_PATH}list")
    current_list=${current_list#"["}
    current_list=${current_list%"]"}

    ## If the list is not empty, add a comma and space.
    if [[ -n $current_list ]]; then
        current_list="$current_list, "
    fi

    updated_list="[$current_list'$C_UUID']"

    echo "${C_INFO}Adding profile to list of profiles..."
    dconf write "${C_DCONF_PATH}list" "$updated_list"

    echo "${C_INFO}Verifying profile was added..."
    if ! check_profile_in_list; then
        echo "${C_ERROR}Profile failed to add to list"
        exit 1
    fi
}

####
# Set the profile as the default profile.
set_profile_as_default() {
    echo "${C_INFO}Setting profile as default..."
    dconf write "${C_DCONF_PATH}default" "'$C_UUID'"

    echo "${C_INFO}Verifying profile was set as default..."
    if ! check_profile_default; then
        echo "${C_ERROR}Profile failed to set as default"
        exit 1
    fi
}


####[ Main ]############################################################################


if [[ $(uname -s) != "Linux" ]]; then
    echo "${C_ERROR}This script currently only works on Linux"
    exit 1
fi


echo "${C_INFO}Checking if profile is loaded..."
if check_profile_loaded; then
    echo "${C_SUCCESS}Profile is loaded"
else
    echo "${C_WARNING}Profile is not loaded"
    load_profile
fi

echo "${C_INFO}Checking if profile is in list..."
if check_profile_in_list; then
    echo "${C_SUCCESS}Profile is in list"
else
    echo "${C_WARNING}Profile is not in list"
    add_profile_to_list
fi

echo "${C_INFO}Checking if profile is default..."
if check_profile_default; then
    echo "${C_SUCCESS}Profile is default"
else
    echo "${C_WARNING}Profile is not default"
    set_profile_as_default
fi
