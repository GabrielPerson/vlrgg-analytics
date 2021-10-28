#!/bin/bash
TEAMS=(gamelanders black_dragons pain havan imperial ingaming vikings vorax furia rise sharks slick)

for team in ${TEAMS[@]}; do
    
    echo ${team}
    urls_path="../urls/"
    out_type="csv"
    team_folder=""

    urls_path+="${team}.txt" #../urls/team.txt
    team_folder+="${team}/" #team/
    team_folder+="${team}" #team/team

    #echo ${urls_path}
    #echo ${team_folder}

    python3 file_input_economy.py ${urls_path} ${team_folder} ${out_type}
done