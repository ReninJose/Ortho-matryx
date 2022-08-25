// Author: Delbert Edric
// Rev 1.0
// Code reads user button input and compares to correct layout to tally

#include <iostream>
#include <ctime> 
#include <bits/stdc++.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

using namespace std;

// # of buttons

const char* PATH = "/home/pyfitl/Documents/Ortho-matryx/backend/color_rand_gen/correct_color.txt";
const char* SCORE = "/home/pyfitl/Documents/Ortho-matryx/backend/color_rand_gen/score.txt";


int main()
{


    int correct_color_index = 0;
    char correct_color;
    int tally = 0;
    string correct_pattern;

    ifstream color_read(PATH, ios::app);
    ofstream score_rewrite(SCORE, ios::trunc);
    ifstream score_read(SCORE, ios::app);
    ofstream score_write(SCORE, ios::app);

    // reading user inputs here. For now static.
    string button_pressed[] = {"B9", "B1", "B5"};

    for(int itr = 0; itr < 3; itr ++){
        button_pressed[itr].erase(0,1);
    }

    // reading correct configuration
    if (!color_read) {
        perror("File not found");
        return 1;
    }

    else{
        
        color_read.clear();
        color_read.seekg(0);
        getline(color_read, correct_pattern);
        color_read.close();

    }
  
    

    // Picks random color from rgb.
    srand((int)time(0));
    correct_color_index = (rand()%3);
    if (correct_color_index == 0){
        correct_color = 'r';
        cout << "\nChosen Colour is Red\n";
    }
    else if (correct_color_index == 1){
        correct_color = 'g';
        cout << "\nChosen Colour is Green\n";
    }
    else{
        correct_color = 'b';
        cout << "\nChosen Colour is Blue\n";
    }



    for (int itr = 0; itr < 3; itr ++){
        int index_tally = stoi(button_pressed[itr]);

        if (correct_pattern[index_tally-1] == correct_color){
            tally= tally + 1;
            
        }
    
    }
    
    if (!score_read) {
        perror("File not found");
        return 1;
    }

    else{
        if (tally == 0){
            cout << "You suck at this game\n";
            score_write << 0;

        }
        else{
            cout << "Your score is: " << tally << '\n';
            score_write << tally;
        }

    }

    score_write.close();
    

    return 0;
}

