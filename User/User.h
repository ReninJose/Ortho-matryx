#ifndef USER_H
#define USER_H

#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <vector>

using namespace std;

class user {
    public:
        // Constructor
        user();
        // Modifiers
        void set_username(char* &name);
        void set_password(char* &passW);
        // Accessors
        char* get_username();
        char* get_password();

    private:
        char* username;
        char* password;
};

class account {
    public:
        // Constructor
        account();

        // Methods
        void create(string &name, string &passW);
        void find_and_login(string &name, string &passW);
    
    private:
        vector<user> u; 
};

#endif