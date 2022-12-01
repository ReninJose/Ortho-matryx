# Author: Ellis Hobby
# Rev 1.0
# !/bin/bash

green='\e[1;32m'
yellow='\e[1;33m'
red='\e[1;31m' 
NC='\e[0m'

SCRIPT=$(readlink -f $0)
MAIN_DIR=$(dirname $SCRIPT)

STARTUP_SCRIPT_EXEC="Exec=/usr/bin/bash ${MAIN_DIR}/startup.sh"
STARTUP_SCRIPT="bash ${MAIN_DIR}/startup.sh"
DEPENDENCIES_SCRIPT="${MAIN_DIR}/dependencies.sh"
CLEAN_SCRIPT="${MAIN_DIR}/clean.sh"
APPLICATION="${MAIN_DIR}/gui-app/app.py"

cd $MAIN_DIR

if [ ! -f "installed.txt" ]; then

	chmod 0777 startup.sh
	chmod 0777 clean.sh
	chmod 0777 dependencies.sh

    cd /etc/xdg/autostart
	sudo touch display.desktop
	ls
	
	echo -e "${green}INSTALLING STARTUP RESOURCES...${NC}"
	sudo echo "[Desktop Entry]" >> display.desktop
	sudo echo "Name=OrthoMatryxGame" >> display.desktop
	sudo echo $STARTUP_SCRIPT_EXEC >> display.desktop
	
	cd $MAIN_DIR
	echo -e "${green}CLEANING DIRECTORY...${NC}"
	sudo bash $CLEAN_SCRIPT
	
	echo -e "${green}INSTALLING DEPENDENCIES...${NC}"
	sudo bash $DEPENDENCIES_SCRIPT
	
	echo -e "${green}INSTALL COMPLETE...${NC}"
	touch "installed.txt"
	echo "Install Complete" >> installed.txt
	
	echo -e "${green}RESTARTING DEVICE...${NC}"
	sudo reboot now
	
fi
