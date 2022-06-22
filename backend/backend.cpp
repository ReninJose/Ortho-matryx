// Author: Renin Kingsly Jose

#include<iostream>
#include<pthread.h>

using namespace std;

string test_id = "4098";
string test_score = "7";

void* score_board(void*) {
    system("cd sb/ && ./sb " + test_id + test_score);
    return NULL;
}

int main(){

    pthread_t call_sb;

    // Calling sb_generator.cpp
    pthread_create(&call_sb, NULL, score_board, NULL);
    pthread_join(call_sb,NULL);

    return 0;
}