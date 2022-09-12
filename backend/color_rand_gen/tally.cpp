// Author: Delbert Edric, Renin Kingsly Jose
// Rev 1.0

// ASSUMING ARGV[1] IS A STRING OF 3 LETTERS ANYWHERE FOR Q-C (REMOVE THIS ONCE THIS PROGRAM IS DONE)

/* ------------------------------------------

"tally.cpp" compares user's inputs and counts scores of a game round and increments it, then stores it on "score.txt". 
 Must be called after color_generator.cpp

------------------------------------------ */

#include <fstream>
#include <map>
#include "shuffle.h"

using namespace std;

const char* color_PATH = "/home/renin/Documents/Ortho-matryx/backend/color_rand_gen/color_pattern.txt";

const char* score_PATH = "/home/renin/Documents/Ortho-matryx/backend/color_rand_gen/score.txt";

const char* cc_PATH = "/home/renin/Documents/Ortho-matryx/backend/color_rand_gen/cc.txt";

int main(int argc, char* argv[]) {

    char cc;                    // cc -> Correct Color
    int cache, score = 0;
    string color_pattern, u_input; 
    
    // USER INPUT MASKING (DO NOT CHANGE)
    map<char, int> mask;
    mask['q'] = 0;
    mask['w'] = 1;
    mask['e'] = 2;
    mask['a'] = 3;
    mask['s'] = 4;
    mask['d'] = 5;
    mask['z'] = 6;
    mask['x'] = 7;
    mask['c'] = 8;

    // File Objects
    ofstream score_write(score_PATH, ios::out);
    ifstream score_check(score_PATH, ios::in);
    ifstream color_read(color_PATH, ios::in);
    ifstream cc_read(cc_PATH, ios::in);
    
    if (!cc_read) {
        perror("cc.txt does not exist or unable to read");
        return 1;
    }
    else {
        cc = color_read.get();                
    }

    if (!color_read) {
        perror("color_pattern.txt does not exist or unable to read");
        return 1;
    }
    else {
        color_read.seekg(0);
        getline(color_read, color_pattern);  
    }

    cc_read.close();
    color_read.close();

    if (!score_check) {
        perror("score.txt does not exist or unable to read");
        return 1;
    }
    else {
        score_check.clear();
        score_check.seekg(0);
        
        score_check >> cache;
        cout << cache << endl;

        u_input = argv[1];
        
        for (int i = 0; i < u_input.length(); i++) {
            if (cc == color_pattern.at(mask.at(u_input.at(i)))) {
                score += 1;
            }
            else continue;
        }
        cout << score << endl;
        score_write << score;

        score_check.close();
        score_write.close();
    }

    return 0;
}

