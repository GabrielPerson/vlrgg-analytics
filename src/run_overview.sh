#!/bin/bash
TEAMS=("gamelanders" "black_dragons" "pain" "havan" "imperial" "ingaming" "vikings" "vorax")

for team in $TEAMS 
do 
    urls_path="../urls/"
    out_type="csv"

    urls_path+="${team}.txt" #../urls/gamelanders.txt
    team_folder+="${team}/" #gamelanders/gamelanders
    team_folder+="${team}"

    #echo ${urls_path}
    #echo ${team_folder}

    #mkdir ${team}
    python3 file_input_overview.py ${urls_path} ${team_folder} ${out_type} 
done