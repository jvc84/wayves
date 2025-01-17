#!/bin/bash

string="$(playerctl -l)"
lines=(${string//\\n/\ })
status="Paused"

for line in "${lines[@]}"; do
    status="$(playerctl status --player="$line")"
    if [[ $status == *"Play"* ]]; then
      break
    fi
done



