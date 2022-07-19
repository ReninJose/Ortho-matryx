// Author: Renin Kingsly Jose, Delbert Edric
// Rev 1.2

#include<bits/stdc++.h>
#include<iostream>
#include<fstream>
#include<forward_list>

using namespace std;

// NOTE: PATH needs to be changed when importing the code to rapsberry pi. 
const char* PATH = "/home/renin/Documents/Ortho-matryx/backend/score_board/sb.txt";

// To group player's attributes
class player {
    public:
        string name;
        int score;
};

// Ascending Ordering the list
bool A_sorter(player a, player b) {   
    return a.score <= b.score;
}

// Descending Ordering the list
bool D_sorter(player a, player b) {
    return a.score >= b.score;
}

// Rearrange and import data back to file
void rearrage_import(forward_list<player> pool) {
    
    ofstream sb_rewrite(PATH, ios::trunc);
    int size = 0;

    // Find # of contents of scoreboard
    for(auto itr: pool){
        size += 1;
    }
    
    //Checks see if scoreboard is fully populated (10)
    if (size > 10) {
        pool.sort(A_sorter);
        pool.pop_front(); 
        pool.sort(D_sorter);
    }
    else {
        pool.sort(D_sorter);
    }

    //Rewrite text file to contain top 10 descending scores.
    for(auto itr: pool) {
        sb_rewrite << itr.name << " " << itr.score << endl;
    }
       
    sb_rewrite.close();

}

int main(int argc, char* argv[]){

    forward_list<player> player_list;
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
    
        while(getline(sb_read, score_line)) {
            // Load in each player to the linked list
            istringstream ss(score_line);
            ss >> player_name;
            p_copy.name = player_name;
            ss >> player_score;
            p_copy.score = player_score;
            player_list.push_front(p_copy);
        }
        // Load in the newest player to the linked list
        p_copy.name = argv[1];
        p_copy.score = stoi(argv[2]);
        player_list.push_front(p_copy);
        
        sb_write.close();
        
        // Rearrange and import data 
        rearrage_import(player_list);  
        sb_read.close();
        return 0;
    }

}