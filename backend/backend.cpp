// Author: Renin Kingsly Jose

#include<iostream>
#include<stdlib.h>
#include<unistd.h>
#include<pthread.h>

using namespace std;

const char* test_id = "john";
const char* test_score = "9";

void* score_board(void*) {      
    execlp("./score_board/sb", "sb", test_id, test_score , NULL);
    return NULL;
}

int main(){

    pthread_t call_sb;
    
    // Calling sb_generator.cpp
    pthread_create(&call_sb, NULL, score_board, NULL);
    pthread_join(call_sb,NULL);

    return 0;
}