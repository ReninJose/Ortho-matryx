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

echo -e "${red}REMOVING MISC....${NC}"
sudo apt remove vim -y

#----Build Project----#
echo -e "${red}DESTROYING EXECUTABLES....${NC}"
cd backend/score_board/
rm sb

if [ -f "sb.txt" ]; then
    echo -e "${yellow}WARNING: REMOVING SB.TXT....${NC}"
    rm -f sb.txt
fi

cd ..
rm backend