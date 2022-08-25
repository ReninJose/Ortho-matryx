// Author: Renin Kingsly Jose
// Rev 2.5

#include<iostream>
#include<string>
#include<stdlib.h>
#include<unistd.h>
#include<sys/wait.h>

using namespace std;

int main(int argc, char* argv[]){

    pid_t pid;              // For process ID 
    int status;
    string command = argv[1];

    // Initiate code for scoreboard
    if (command.compare("sb") == 0) {
        
        if (argc != 4) {
            cout << "Invalid # of argument count" << endl;
            return 1;
        }

        const char* id;
        const char* score;

        id = argv[2];
        cout << id;
        score = argv[3];
        cout << " " << score << endl;

        if(execl("/home/renin/Documents/Ortho-matryx/backend/score_board/sb", "sb", id, score , NULL) < 0) {
            perror("Execl failed");
            return 1;
        }    
    }
    // Initiate code for Color Generator
    else if (command.compare("cg") == 0) {
        pid = fork();                   // Forking new process

        if(pid < 0) {
            perror("Fork failed");
            return 1;
        }

        // Child
        if(pid == 0) {
            if(execl("/home/renin/Documents/Ortho-matryx/backend/color_rand_gen/color", "color", NULL) < 0) {
                perror("Execl failed");
                return 1;
            }
        }
        // Parent
        else if(pid > 0) {
            // Wait for child process to finish
            wait(&status);

            // This section executes piClient.py
            if (execl("/home/renin/Documents/Ortho-matryx/pi-client/Initiator", "Initiator", NULL) < 0) {            // FINISH THIS
                perror("Execl failed");
                return 1;
            }
        }    
    }
    return 0;
}