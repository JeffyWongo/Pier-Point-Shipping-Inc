// main.cpp
#include "Balance.h"
#include <iostream>
#include <vector>

using namespace std;

int main() {

    vector<vector<int>> ship(8, vector<int>(12, 0));

    Balance balance(ship);

    // test data
    /*  //this is the bug case - not yet solved
    balance.modifyShip(7, 2, 10);
    balance.modifyShip(7, 7, 15);
    balance.modifyShip(7, 5, 20);
    balance.modifyShip(7, 6, 5);
    balance.printShip();
    */

    /*
    //test case1
    balance.modifyShip(7, 0, -1);
    balance.modifyShip(7, 1, -1);
    balance.modifyShip(7, 2, -1);
    balance.modifyShip(7, 9, -1);
    balance.modifyShip(7, 10, -1);
    balance.modifyShip(7, 11, -1);
    balance.modifyShip(6, 11, -1);
    balance.modifyShip(7, 1, 99);
    balance.modifyShip(7, 2, 100);
    */

    /*
    //test case2
    balance.modifyShip(7, 3, 120);
    balance.modifyShip(7, 8, 35);
    balance.modifyShip(6, 2, 50);
    balance.modifyShip(5, 0, 40);
    */

    
    //test case3
    balance.modifyShip(7, 0, 10001);
    balance.modifyShip(7, 1, 500);
    balance.modifyShip(7, 2, 600);
    balance.modifyShip(7, 3, 100);
    balance.modifyShip(6, 0, 9041);
    balance.modifyShip(6, 1, 10);
    

    /*
    //test case4
    balance.modifyShip(7, 0, -1);
    balance.modifyShip(7, 1, -1);
    balance.modifyShip(7, 2, -1);
    balance.modifyShip(7, 3, -1);
    balance.modifyShip(7, 4, -1);
    balance.modifyShip(7, 5, -1);
    balance.modifyShip(7, 6, -1);
    balance.modifyShip(7, 7, -1);
    balance.modifyShip(7, 8, -1);
    balance.modifyShip(7, 9, -1);
    balance.modifyShip(7, 10, -1);
    balance.modifyShip(7, 11, -1);
    balance.modifyShip(6, 4, 2000);
    balance.modifyShip(6, 11, -1);
    balance.modifyShip(5, 4, 2007);
    balance.modifyShip(4, 4, 2011);
    balance.modifyShip(3, 4, 10000);
    balance.modifyShip(2, 4, 2020);
    balance.modifyShip(1, 4, 1100);
    balance.modifyShip(0, 4, 3044);
    */

    /*
    //test case5
    balance.modifyShip(7, 0, -1);
    balance.modifyShip(7, 1, 96);
    balance.modifyShip(7, 2, 8);
    balance.modifyShip(7, 3, 4);
    balance.modifyShip(7, 4, 4);
    balance.modifyShip(7, 5, 1);
    balance.modifyShip(7, 11, -1);
    */

    /*
    //test case SilverQueen
    balance.modifyShip(7, 0, -1);
    balance.modifyShip(7, 1, 60);
    balance.modifyShip(7, 2, 20);
    balance.modifyShip(7, 3, 20);
    balance.modifyShip(7, 11, -1);
    balance.modifyShip(6, 1, 20);
    */


    balance.printShip();

    while (!balance.isBalanced()) {
        balance.calculateSums();
        balance.printBestMove();
        balance.printShip();
    }

    cout << "Congrats! it's balanced now." << endl;

    return 0;
}
