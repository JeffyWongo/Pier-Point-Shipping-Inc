// main.cpp
#include "Balance.h"
#include <iostream>
#include <vector>

using namespace std;

int main() {
    vector<vector<int>> ship(8, vector<int>(12, 0));
    ship[3][2] = 10;  // element on the left to test
    ship[3][4] = 10;  // test case to block the route
    ship[2][5] = 10;  // test case to block the route
    ship[5][10] = 5;  // element on the right to test
    ship[5][7] = 15;  // test case to block the route

    Balance balance(ship);

    balance.printShip();

    //test from left to right
    int testX = 3;
    int testY = 2;
    cout << "\ntest moving block [" << testX << "][" << testY << "] from left to right：" << endl;
    auto path1 = balance.findShortestPath(3, 2); // test [3][2]
    if (!path1.empty()) {
        cout << "successful! here's the route：" << endl;
        for (size_t i = 0; i < path1.size(); ++i) {
            cout << "Step " << i + 1 << ": (" << path1[i].first << ", " << path1[i].second << ")" << endl;
        }
    }
    else {
        cout << "failed, can't find a route" << endl;
    }


    //test from right to left
    testX = 5;
    testY = 10;
    cout << "\ntest moving block [" << testX << "][" << testY << "] from right to left：" << endl;
    auto path2 = balance.findShortestPath(5, 10); // test [5][10]
    if (!path2.empty()) {
        cout << "successful, here's the route：" << endl;
        for (size_t i = 0; i < path2.size(); ++i) {
            cout << "Step " << i + 1 << ": (" << path2[i].first << ", " << path2[i].second << ")" << endl;
        }
    }
    else {
        cout << "failed, can't find a route" << endl;
    }

    return 0;
}
