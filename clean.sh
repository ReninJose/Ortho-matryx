# Author: Renin Kingsly Jose
# Rev 1.0
# !/bin/bash

green='\e[1;32m'
yellow='\e[1;33m'
red='\e[1;31m' 
NC='\e[0m'

# ---- Update system ----#
echo -e "${green}UPDATING SYSTEM....${yellow}"
sudo apt update
sudo apt upgrade -y

#----Remove Project----#
echo -e "${red}DESTROYING EXECUTABLES....${NC}"
cd backend/score_board/
rm sb
echo -e "${yellow}WARNING: REMOVING SB.TXT....${NC}"
rm sb.txt

cd ..
rm backend
cd color_rand_gen/
rm color_generator
rm tally
echo -e "${YELLOW}WARNING: REMOVING CORRECT_COLOR.TXT, AND SCORE.TXT....${NC}"
rm *.txt

cd /home/renin/Documents/Ortho-matryx/pi-client/
rm Initiator
echo -e "${yellow}WARNING: REMOVING BATTERY.TXT, BUTTON.TXT, AND RANDOM.TXT....${NC}"
rm *.txt

#---END---#