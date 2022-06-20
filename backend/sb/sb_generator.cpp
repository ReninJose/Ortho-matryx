// Author: Renin Kingsly Jose

#include<iostream>
#include<fstream>
#include<cstdio>

using namespace std;

int main(int argc, char* argv[]){

    int id = stoi(argv[1]);
    int score = stoi(argv[2]);

    // Opening sb.txt
    fstream sb;
    sb.open("sb.txt");
    if (!sb.is_open()) {
        perror("File not found");
    }

    cout << "ID: " << id << endl;
    cout << "Score: " << score << endl;

    sb.close();

    return 0;
}