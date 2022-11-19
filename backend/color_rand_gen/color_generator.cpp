// Author: Delbert Edric, Renin Kingsly Jose
// Rev 2.0

/* ------------------------------------------

"color_generator.cpp" generates randomized pattern of colors for each game round and picks the correct color.

------------------------------------------ */

#include <fstream>
#include <iostream>
#include <bits/stdc++.h>   

using namespace std;

// # of buttons
#define SIZE 9

const char* color_PATH = "/home/eldunno/capstone/Ortho-matryx/backend/color_rand_gen/color_pattern.txt";

const char* cc_PATH = "/home/eldunno/capstone/Ortho-matryx/backend/color_rand_gen/correct_color.txt";


char* shuffle_array(char arr[], int n)
{
    // To obtain a time-based seed
    unsigned seed = rand();
 
    // Shuffling array
    shuffle(arr, arr + n, std::default_random_engine(seed));

    return arr;
}

int main() {
    
    srand(time(NULL));
    char* color_randomized;
    char colors[] = {'r','r','r','g','g','g','b','b','b'};
    char correct_color;

    ifstream color_read(color_PATH, ios::in);
    ofstream color_write(color_PATH, ios::out );

    ifstream cc_read(cc_PATH, ios::in);
    ofstream cc_write(cc_PATH, ios::out);

    // Shuffle colors
    color_randomized = shuffle_array(colors, SIZE);

    // Opening correct_color.txt
    if (!color_read) {
        perror("File not found");
        return 1;
    }
    else{
        color_write << color_randomized;
    }

    color_read.close();
    color_write.close();

    // Pick a color randomly from color_picker
    correct_color = color_randomized[(rand() % 9)];

    // Opening cc.txt
    if (!cc_read) {
        perror("File not found");
        return 1;
    }
    else {
        cc_write << correct_color;
    }

    cc_read.close();
    cc_write.close();

    return 0;
}
