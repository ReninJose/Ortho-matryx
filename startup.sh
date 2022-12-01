
#Author: Renin Kingsly Jose, Ellis Hobby
#Rev 1.1
#!/bin/bash

export DISPLAY=:0

# Get directory for game
SCRIPT=$(readlink -f $0)
MAIN_DIR=$(dirname $SCRIPT)

# Run application
cd $MAIN_DIR
cd gui-app/
python3 app.py
