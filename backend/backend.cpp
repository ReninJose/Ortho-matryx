// Author: Renin Kingsly Jose
// Rev 2.5

/* ------------------------------------------

Backend.cpp allows front-end modules to send arguments to the back-end module to perform the following functions

Generate per game round's color pattern:
    - ./backend cg 

Adding contents to the scoreboard:
    - ./backend sb <(name)id> <score> 

------------------------------------------ */ 

#include<iostream>
#include<string>
#include<stdlib.h>
#include<unistd.h>
#include<sys/wait.h>

using namespace std;

const char* sb_PATH = "/home/eldunno/capstone/Ortho-matryx/backend/score_board/sb";
const char* cg_PATH = "/home/eldunno/capstone/Ortho-matryx/backend/color_rand_gen/color_generator";


int main(int argc, char* argv[]){

    int status;
    string command = argv[1];

    // Initiate code for scoreboard
    if (command.compare("sb") == 0) {
        
        if (argc != 5) {
            cout << "Invalid # of argument count" << endl;
            return 1;
        }

        const char* id;
        const char* score;
        const char* avatar;

        id = argv[2];
        score = argv[3];
        avatar = argv[4];

        if(execl(sb_PATH, "sb", id, score , avatar, NULL) < 0) {
            perror("Execl failed");
            return 1;
        }    
    }
    // Initiate code for Color Generator
    else if (command.compare("cg") == 0) {

        if(execl(cg_PATH, "color", NULL) < 0) {
            perror("Execl failed");
            return 1;
        }
    }    

    return 0;
}
    

    
