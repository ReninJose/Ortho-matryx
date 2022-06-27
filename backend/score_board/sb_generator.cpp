// Author: Renin Kingsly Jose

#include<bits/stdc++.h>
#include<iostream>
#include<fstream>
#include<list>

using namespace std;

// NOTE: PATH needs to be changed when importing the code to rapsberry pi. 
const char* PATH = "/home/renin/Documents/Ortho-matryx/backend/score_board/sb.txt";

class player {
    public:
        string name;
        int score;
};

// Need something to print all contents in list

void rearrage(list<player> player_list_copy) {
    // WRITE CODE HERE DEL. Use player_list_copy, Don't worry about rest of the code, just focus on this fuction.
    // This function returns void, so it returns nothing. All I want is arranged data inside player_list_copy.
    // And also remove the comments inside this function after you are done.
}

int main(int argc, char* argv[]){

    list<player> player_list;
    player p_copy;

    string player_name;
    int player_score;
    string score_line;
    
    ifstream sb_read(PATH, ios::app);
    ofstream sb_write(PATH, ios::app);

    // Opening sb.txt
    if (!sb_read) {
        perror("File not found");
        return 1;
    }

    // Check if scoreboard is empty
    if (!getline(sb_read, score_line)) {
        cout << "Scoreboard Empty, Writting first content on the board" << endl;
        // Write first content on the board
        sb_write << argv[1] << " " << stoi(argv[2]) << endl;
        sb_read.close();
        sb_write.close();
        return 0; 
    }
    else {
        // Reseting getline back to first line of the file
        sb_read.clear();
        sb_read.seekg(0);
        cout << "Reading contents from the scoreboard" << endl;
        while(getline(sb_read, score_line)) {
            // Load in each player to the linked list
            istringstream ss(score_line);
            ss >> player_name;
            p_copy.name = player_name;
            ss >> player_score;
            p_copy.score = player_score;
            player_list.push_back(p_copy);
        }
        // Load in the newest player to the linked list
        p_copy.name = argv[1];
        p_copy.score = stoi(argv[2]);
        player_list.push_back(p_copy);
        // Rearrange linked list based on player's score (Descending order)
        rearrage(player_list);
    }

    sb_read.close();
    sb_write.close();

    return 0;
}