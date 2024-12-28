#!/bin/bash

player="$1"
category="$2"
token="$3"


# Functions
terminate() {
    pkill -f "$token" &> /dev/null
}


get_variables() {
    if [[ "$player" == "cava" ]]; then
	      player_status="Playing"
        category="active"
    else
      	player_status="$( playerctl status --player="$player" 2> /dev/null)"
    fi 

    # check_music
    if [ "$player_status" = "Playing" ]; then
        check_music="true"
    else
        check_music="false"
    fi

    # check_player
    if [[ $player_status == "P"* ]]; then
        check_player="true"
    else
        check_player="false"
    fi
}


check_state() {
    get_variables

    while :
    do
      get_variables
        if [ \( "$category" = "off" \) -a \( "$check_player" = "true" \) ] || \
        [ \( "$category" = "inactive" \) -a \( \( "$check_player" = "false" \) -o \( "$check_music" = "true" \) \) ] || \
        [ \( "$category" = "active" \) -a \( \( "$check_player" = "false" \) -o \( "$check_music" = "false" \) \) ]; then
            break
        fi

        sleep 1
    done
}

check_state && terminate
