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
    int calculateHeuristic(int row, int col, int targetRow, int targetCol);
    int leftSum;
    int rightSum;
    int totalSum;
    int rows = 8, cols = 12;
    bool opitimalBalance = false;
    pair<int, int> previousBestMove = { -1, -1 };

public:
    Balance(vector<vector<int>>& initialShip); //constructor
    bool moveObstacle(int row, int col);
    void printShipWeight();
    void calculateSums();
    void modifyShip(int row, int col, int value);
    void printBestMove();
    bool isBalanced();
    int containerWeight(int row, int col);
    vector<pair<int, int>> findShortestPath(int startRow, int startCol);
    pair<int, int> findBestMove();
    void printShip();
};

#endif
