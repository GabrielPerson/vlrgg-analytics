#!/bin/bash
TEAMS=("gamelanders" "black_dragons" "pain" "havan" "imperial" "ingaming" "vikings" "vorax")

for team in $TEAMS 
do 
    urls_path="../urls/"
    out_file="_overview"
    out_type="csv"

    urls_path+="${team}.txt" #../urls/gamelanders.txt
    team_folder+="${team}/" #gamelanders/gamelanders_overview
    team_folder+="${team}${out_file}"

    #echo ${urls_path}
    #echo ${team_folder}

    python3 file_input_overview.py ${urls_path} ${team_folder} ${out_type} 
done