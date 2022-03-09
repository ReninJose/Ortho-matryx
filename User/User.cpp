#include "User.h"

/*------------------------ USER CLASS METHODS -------------------------*/

user::user(){
    ;
}

void user::set_username(char* &name) {
    username = name;
}

void user::set_password(char* &passW){
    password = passW;
}

char* user::get_username() {
    return username;
}

char* user::get_password() {
    return password;
}

/*----------------------- ACCOUNT CLASS METHODS -----------------------*/

account::account(){
    string read_text;
    ifstream read_users;
    user insert_user;
    char* cstr; 
    char* U_name;
    char* input_passW;

    read_users.open("Users.txt", ios::in);

    // Error handling
    if (!read_users.is_open()) {
        cout << "Error: File does not exist" << endl;
        exit(0);
    }

    while (getline(read_users, read_text)){
        cstr = new char [read_text.length()+1];
        strcpy(cstr, read_text.c_str());
        U_name = strtok(cstr, " ");
        input_passW = strtok(NULL, " ");
        insert_user.set_username(U_name);
        insert_user.set_password(input_passW);
        u.push_back(insert_user);
    }

    read_users.close();
}

void account::create(string &name, string &passW) {
    ofstream write_users;

    write_users.open("Users.txt", ios::app);

    // Error handling
    if (!write_users.is_open()) {
        cout << "Error: File Creation failed" << endl;
        exit(0);
    }

    write_users << name << " ";
    write_users << passW << endl;
    write_users.close();
}

void account::find_and_login(string &name, string &passW) {

    bool login = false;

    for (int i = 0; i < u.size(); i++) {
        if (u.at(i).get_username() == name) {
            if (u.at(i).get_password() == passW) {
                cout << "LOGGED IN" << endl;
                login = true;
            }
            else
                cout << "Incorrect Password" << endl;
                exit(0);
        }
    }

    if (login == false) {
        cout << "Username not found or Incorrect Username" << endl;
    }
}

int main(int argc, char** argv) {
    string name;
    string passW;
    account acc;

    cout << "Enter Username: ";
    cin >> name;
    cout << "Enter Password: ";
    cin >> passW;

    if (string(argv[1]) == "LOGIN") { 
        acc.find_and_login(name, passW);
    }
 
    return 0;
}