// Author: Renin Kingsly Jose
// Rev 2.0

#include<iostream>
#include<string>
#include<stdlib.h>
#include<unistd.h>
//#include<pthread.h>
#include<sys/wait.h>

using namespace std;

int main(int argc, char* argv[]){

    pid_t pid;              // For process ID 
    int status;
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
        pid = fork();                   // Forking new process

        if(pid < 0) {
            perror("Fork failed");
            return 1;
        }

        // Child
        if(pid == 0) {
            if(execl("/home/pyfitl/Documents/Ortho-matryx/backend/score_board/sb", "sb", id, score , NULL) < 0) {
                perror("Execl failed");
                return 1;
            }    
        }
        // Parent
        else {
            // Parent waits until child process ends
            wait(&status);
        }
    }
    // Initiate code for Color Generator
    else if (command.compare("cg") == 0) {
        // open color generator code & and most likely keep the backend thread running.
    }


    return 0;
}
