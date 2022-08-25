// Author: Delbert Edric, Renin Kingsly Jose
// Rev 1.1

#include <iostream>
#include <ctime> 
#include <bits/stdc++.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include<fstream>

using namespace std;

// # of buttons
#define SIZE 9

const char* PATH = "/home/pyfitl/Documents/Ortho-matryx/backend/color_rand_gen/correct_color.txt";
char colors[] = {'r','r','r','g','g','g','b','b','b'};
char picker[] = {'0','1','2','3','4','5','6','7','8'};

int i;

// Prints in a manner that simulates the terminal of buttons (Only for development purpose)
void print_array(int array[], int n) {

    i = 1;

    for(int itr = 0; itr < n; itr++) {
        cout << array[itr] << " ";
        if (i == 3) {
            cout << endl;
            i = 0;
        }
        i++;
    }
}

// Shuffle array
char* shuffle_array(char arr[], int n)
{
    // To obtain a time-based seed
    srand((int)time(0));
    unsigned seed = (rand()%100);
 
    // Shuffling our array
    shuffle(arr, arr + n, default_random_engine(seed));

    return arr;
}

// Plays the Game
void print_game(int button_num, int size, int picker[], char* randomized){
    int i = 1;
    bool picked = false;
    for (int itr = 0; itr < size; itr++) {
        for (int itr_ = 0; itr_ < button_num; itr_ ++) {
            if (picker[itr_] == itr) {
                cout << randomized[picker[itr_]] << " ";
                picked = true;
                break;
            }
        }

        if (picked != true) {
            cout << "_ ";
        }
        
        if (i == 3) {
            cout << endl;
            i = 0;
        }

        picked = false;
        i++;
    }

    cout << endl;
   
}


int main()
{
    char* color_randomized;
    char* picker_randomized;

    // nine buttons total. Divides them to show half and half

    int picker_1[5];
    int picker_2[4];

    bool picked = false;


    // Shuffle colors
    color_randomized = shuffle_array(colors, SIZE);
    //print_array(color_randomized);

    // Shuffle index picker
    picker_randomized = shuffle_array(picker, SIZE);
    //print_array(picker_randomized, SIZE);

    for (int itr = 0; itr < SIZE; itr++) {
        if (itr < 5) {
            picker_1[itr] = (int)picker_randomized[itr] - 48;       // ASCII STARTS AT 48
        }
        else if (itr >= 5 ) {
            picker_2[itr - 5] = (int)picker_randomized[itr] - 48;
        }
    }


    ifstream color_read(PATH, ios::app);
    ofstream color_write(PATH, ios::app);
    ofstream color_rewrite(PATH, ios::trunc);

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

    print_game(5, SIZE, picker_1, color_randomized);
    sleep(1);
    print_game(4, SIZE, picker_2, color_randomized);
    cout << "\n" << color_randomized << "\n";
   
  
    return 0;
}


   