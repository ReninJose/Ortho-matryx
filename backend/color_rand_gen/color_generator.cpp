// Author: Delbert Edric
// Rev 1.0

#include <iostream>
#include <ctime> 
#include <bits/stdc++.h>
using namespace std;

 
// Shuffle array
void shuffle_array(char arr[], int n)
{
 
    // To obtain a time-based seed
    srand((int)time(0));
    unsigned seed = (rand()%100);
 
    // Shuffling our array
    shuffle(arr, arr + n,
            default_random_engine(seed));
 
    // Printing our array
    for (int i = 0; i < n; ++i)
        cout << arr[i] << " ";
    cout << endl;
}
 
// Driver code
int main()
{
 
    char a[] = { 'r', 'r', 'r', 'g', 'g', 'g','b', 'b', 'b' };

 
    shuffle_array(a, 9);
 
    return 0;
}


   