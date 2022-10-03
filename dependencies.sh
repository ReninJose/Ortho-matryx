# Author: Renin Kingsly Jose
# Rev 2.0
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
sudo apt-get install python-dev -y
sudo apt-get install python3-dev -y  
pip install bleak

# ---- FOR C/C++ ----#
echo -e "${green}INCLUDING C/C++ PACKAGES....${NC}"
sudo apt install gcc -y
sudo apt install g++ -y

#----Build Project----#
echo -e "${green}BUILDING EXECUTABLES....${NC}"
cd backend/score_board/
g++ -o sb sb_generator.cpp

if [ ! -f "sb.txt" ]; then
    echo -e "${yellow}MANIFESTING A NEW SB.TXT....${NC}"
    touch sb.txt
fi

cd ..
g++ -o backend backend.cpp
cd color_rand_gen/
g++ -o color_generator color_generator.cpp

if [ ! -f "correct_color.txt" ]; then
    echo -e "${yellow}MANIFESTING A NEW CORRECT_COLOR.TXT....${NC}"
    touch correct_color.txt
fi

if [ ! -f "scolor_pattern.txt" ]; then
    echo -e "${yellow}MANIFESTING A NEW COLOR_PATTERN.TXT....${NC}"
    touch color_pattern.txt
fi

echo -e "${yellow}CREATING .font/ DIRECTORY....${NC}"
mkdir ~/.fonts/
echo -e "${yellow}COPYING AtariFontFullVersion-ZJ23.ttf TO .fonts/ DIRECTORY....${NC}"
cd /home/eldunno/capstone/Ortho-matryx/gui-app/fonts
cp AtariFontFullVersion-ZJ23.ttf ~/.fonts

echo -e "${yellow}UPDATING FONTS CACHE....${NC}"
fc-cache -f -v 

#---END---#
