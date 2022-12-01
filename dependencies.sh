# Author: Renin Kingsly Jose, Ellis Hobby
# Rev 2.1
# !/bin/bash

green='\e[1;32m'
yellow='\e[1;33m'
red='\e[1;31m' 
NC='\e[0m'

SCRIPT=$(readlink -f $0)
MAIN_DIR=$(dirname $SCRIPT)

cd $MAIN_DIR

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
sudo pip install bleak
sudo pip install pygame

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
    chmod 0777 sb.txt
    echo -e "${yellow}WRITING DEFAULT HIGHSCORES....${NC}"
    echo BOT 50 5 >> sb.txt
    echo OII 40 1 >> sb.txt
    echo PIG 30 2 >> sb.txt
    echo ELL 20 4 >> sb.txt
    echo DEL 15 3 >> sb.txt
    echo CON 10 0 >> sb.txt
    echo RYN 8 5 >> sb.txt
    echo REN 5 0 >> sb.txt
    echo DEV 2 1 >> sb.txt
    
fi

cd ..
g++ -o backend backend.cpp
cd color_rand_gen/
g++ -o color_generator color_generator.cpp

if [ ! -f "correct_color.txt" ]; then
    echo -e "${yellow}MANIFESTING A NEW CORRECT_COLOR.TXT....${NC}"
    touch correct_color.txt
    chmod 0777 correct_color.txt
fi

if [ ! -f "scolor_pattern.txt" ]; then
    echo -e "${yellow}MANIFESTING A NEW COLOR_PATTERN.TXT....${NC}"
    touch color_pattern.txt
    chmod 0777 color_pattern.txt
fi

echo -e "${yellow}CREATING .font/ DIRECTORY....${NC}"
mkdir ~/.fonts/
chmod 0777 .fonts/
echo -e "${yellow}COPYING AtariFontFullVersion-ZJ23.ttf TO .fonts/ DIRECTORY....${NC}"
cd ..
cd ..
cd gui-app/fonts
cp AtariFontFullVersion-ZJ23.ttf ~/.fonts
chmod 0777 AtariFontFullVersion-ZJ23.ttf

echo -e "${yellow}UPDATING FONTS CACHE....${NC}"
fc-cache -f -v 

#---END---#
