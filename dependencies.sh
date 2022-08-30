# Author: Renin Kingsly Jose
# Rev 1.5
# !/bin/bash

green='\e[1;32m'
yellow='\e[1;33m'
red='\e[1;31m' 
NC='\e[0m'

# ---- Update system ----#
echo -e "${green}UPDATING SYSTEM....${yellow}"
sudo apt update
sudo apt upgrade -y

echo -e "${green}INSTALLING MISC....${NC}"
sudo apt install vim -y

# ---- FOR PYTHON ----#
echo -e "${green}INCLUDING PYTHON PACKAGES....${NC}"
sudo apt install python3 -y
sudo apt install python3-pil python3-pil.imagetk -y

# ---- FOR C/C++ ----#
echo -e "${green}INCLUDING C/C++ PACKAGES....${NC}"
sudo apt install gcc -y
sudo apt install g++ -y

#----Build Project----#
echo -e "${green}BUILDING EXECUTABLES....${NC}"
cd backend/score_board/
g++ -o sb sb_generator.cpp

if [ ! -f "sb.txt" ]; then
    echo -e "${yellow}WARNING: MANIFESTING A NEW SB.TXT....${NC}"
    touch sb.txt
fi

cd ..
g++ -o backend backend.cpp