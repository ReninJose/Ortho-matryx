// Author: Renin Kingsly Jose

#include<iostream>
#include<stdlib.h>
#include<unistd.h>
//#include<pthread.h>
#include<string>

using namespace std;

int main(int argc, char* argv[]){

    const char* id;
    const char* score;
    string command = argv[1];

    if (argc != 4) {
        cout << "Invalid # of argument count" << endl;
        return 1;
    }
    // Initiate code for scoreboard
    if (command.compare("sb") == 0) {
        id = argv[2];
        cout << id;
        score = argv[3];
        cout << " " << score << endl;
        cout << "Process overlaying sb_generator.cpp over backend.cpp ..." << endl;
        execlp("./score_board/sb", "sb", id, score , NULL);     // Calling execlp ends this program here
    }
    // Initiate code for Color Generator
    else if (command.compare("cg") == 0) {
        // open color generator code & and most likely keep the backend thread running.
    }


    return 0;
}