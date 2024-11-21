#pragma once
// Balance.h
#ifndef BALANCE_H
#define BALANCE_H

#include "Node.h"
#include <vector>
#include <string>
using namespace std;

class Balance {
private:
    vector<vector<int>> ship; // 2d vector of int (weight)
    int calculateHeuristic(int row, int col, bool moveToRight);

public:
    Balance(vector<vector<int>>& initialShip); //constructor
    vector<pair<int, int>> findShortestPath(int startRow, int startCol);
    void printShip();
};

#endif
