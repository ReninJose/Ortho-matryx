// Author: Renin Kingsly Jose, Ellis Hobby
// Rev 2.6

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



int main(int argc, char* argv[]){
    
    string main_dir = argv[2];
    string sb_dir = main_dir;
    string cg_dir = main_dir;
    const char* sb_PATH;
    const char* cg_PATH;
    const char* DIR = main_dir.c_str();
        
    sb_PATH = sb_dir.append("backend/score_board/sb").c_str();
    cg_PATH = cg_dir.append("backend/color_rand_gen/color_generator").c_str();
    
    cout << main_dir << endl;
    cout << sb_PATH << endl;
    cout << cg_PATH << endl;

    
    string command = argv[1];
    
    cout << argc << endl;

    // Initiate code for scoreboard
    if (command.compare("sb") == 0) {
        
        if (argc != 6) {
            cout << "Invalid # of argument count" << endl;
            return 1;
        }

        const char* id;
        const char* score;
        const char* avatar;

        id = argv[3];
        score = argv[4];
        avatar = argv[5];

        if(execl(sb_PATH, "sb", id, score , avatar, DIR, NULL) < 0) {
            perror("Execl failed");
            return 1;
        }    
    }
    // Initiate code for Color Generator
    else if (command.compare("cg") == 0) {

        if(execl(cg_PATH, "color_generator", DIR, NULL) < 0) {
            perror("Execl failed");
            return 1;
        }
    }    

    return 0;
}
    

    
