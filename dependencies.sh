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
g++ -o tally tally.cpp

if [ ! -f "correct_color.txt"]; then
    echo -e "${yellow}MANIFESTING A NEW CORRECT_COLOR.TXT....${NC}"
    touch correct_color.txt
fi

if [ ! -f "score.txt"];then
    echo -e "${yellow}MANIFESTING A NEW SCORE.TXT....${NC}"
    touch score.txt
fi

cd ../../pi-client/
gcc -o Initiator Initiator.c $(/usr/bin/python2.7-config --ldflags)

if [ ! -f "battery.txt"]; then
    echo -e "${yellow}MANIFESTING A NEW BATTERY.TXT....${NC}"
    touch correct_color.txt
fi

if [ ! -f "random.txt"];then
    echo -e "${yellow}MANIFESTING A NEW RANDOM.TXT....${NC}"
    touch score.txt
fi

if [ ! -f "button.txt"];then
    echo -e "${yellow}MANIFESTING A NEW BUTTON.TXT....${NC}"
    touch button.txt
fi

#---END---#