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
echo -e "${yellow}WARNING: REMOVING CORRECT_COLOR.TXT, AND COLOR_PATTERN.TXT....${NC}"
rm *.txt

cd ~/
echo -e "${yellow}WARNING: REMOVING FONTS....${NC}"
rm -r .fonts/

#---END---#
