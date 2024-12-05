// Balance.cpp
#include "Balance.h"
#include <iostream>
#include <queue>
#include <unordered_map>
#include <cmath>
#include <iomanip>
#include <string>

using namespace std;

Balance::Balance(vector<vector<int>>& initialShip) : ship(initialShip) {}

int Balance::calculateHeuristic(int row, int col, int targetRow, int targetCol) {
    return abs(row - targetRow) + abs(col - targetCol);
}


vector<pair<int, int>> Balance::findShortestPath(int startRow, int startCol) {
    priority_queue<Node, vector<Node>, greater<Node>> openList;
    unordered_map<string, bool> visited;
    vector<pair<int, int>> directions = { {-1, 0}, {1, 0}, {0, -1}, {0, 1} };

    bool moveToRight = (startCol < cols / 2);

    int targetCol = moveToRight ? cols / 2 : cols / 2 - 1;
    int targetRow = -1;

    if (moveToRight) {

        while (targetCol >= cols / 2 && targetCol < cols) {
            for (int r = rows - 1; r >= 0; --r) { // from the bottom row
                if (ship[r][targetCol] == 0) {
                    // no floating container check
                    if (r == rows - 1 || ship[r + 1][targetCol] != 0) {
                        targetRow = r;
                        break;
                    }
                }
            }
            if (targetRow != -1) break;
            --targetCol;
        }
    }
    else {
        while (targetCol >= 0 && targetCol < cols / 2) {
            for (int r = rows - 1; r >= 0; --r) { // from the bottom row
                if (ship[r][targetCol] == 0) {
                    // no floating container check
                    if (r == rows - 1 || ship[r + 1][targetCol] != 0) {
                        targetRow = r;
                        break;
                    }
                }
            }
            if (targetRow != -1) break; 
            ++targetCol;
        }
    }

    if (targetRow == -1) {
        cout << "can't find target。" << endl;
        return {};
    }


    Node startNode = { startRow, startCol, 0, calculateHeuristic(startRow, startCol, targetRow, targetCol), {} };
    openList.push(startNode);

    while (!openList.empty()) {
        Node current = openList.top();
        openList.pop();

        if (current.row == targetRow && current.col == targetCol) {
            return current.path;
        }

        string state = to_string(current.row) + "-" + to_string(current.col);
        if (visited[state]) continue;
        visited[state] = true;

        for (auto& dir : directions) {
            int newRow = current.row + dir.first;
            int newCol = current.col + dir.second;
            if (newRow < 0 || newRow >= rows || newCol < 0 || newCol >= cols) continue;
            if (visited[to_string(newRow) + "-" + to_string(newCol)]) continue;
            if (ship[newRow][newCol] != 0) continue; 


            int newG = current.g + 1;
            int newH = calculateHeuristic(newRow, newCol, targetRow, targetCol);

            Node newNode = { newRow, newCol, newG, newH, current.path };
            newNode.path.push_back({ newRow, newCol });
            openList.push(newNode);
        }
    }

    return {};
}



void Balance::calculateSums() {
    leftSum = 0;
    rightSum = 0;
    totalSum = 0;

    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            if(ship[i][j] == -1){} // if it's NAN then ignore it
            else {
                totalSum += ship[i][j];
                if (j < cols / 2) {
                    leftSum += ship[i][j];
                }
                else {
                    rightSum += ship[i][j];
                }
            }
        }
    }

    cout << "weights on left half: " << leftSum << endl;
    cout << "weights on right half: " << rightSum << endl;
    cout << "total weight: " << totalSum << endl;
}


void Balance::modifyShip(int row, int col, int value) {
    ship[row][col] = value;
}


int Balance::containerWeight(int row, int col) {
    return ship[row][col];
}


bool Balance::isBalanced() {
    if (opitimalBalance == true) {
        return true;
    }

    calculateSums();


    int totalWeight = leftSum + rightSum;


    if (totalWeight == 0) {
        return true;
    }

    int tolerance = totalWeight * 0.1; // 10%

    return abs(leftSum - rightSum) <= tolerance;
}





// print the best move route
void Balance::printBestMove() {
    pair<int, int> bestMove = findBestMove();

    if (previousBestMove == bestMove)
    {
        cout << "opitimal balance achived!" << endl;
        opitimalBalance = true;
        return;
    }
    else
    {
        int row = bestMove.first;
        int col = bestMove.second;

        auto path1 = findShortestPath(row, col);
        if (!path1.empty()) {
            cout << "target position:[" << row << "][" << col << "] = " << containerWeight(row, col) << endl;
            cout << "successful! here's the route：" << endl;
            for (size_t i = 0; i < path1.size(); ++i) {
                cout << "Step " << i + 1 << ": (" << path1[i].first << ", " << path1[i].second << ")" << endl;
            }
            modifyShip(path1[path1.size() - 1].first, path1[path1.size() - 1].second, containerWeight(row, col)); //move the weight
            previousBestMove = { path1[path1.size() - 1].first, path1[path1.size() - 1].second };
            modifyShip(row, col, 0); // clear origin spot
        }
        else {
            cout << "failed, can't find a route" << endl;
        }
    }
}

//find which is the best target to move
pair<int, int> Balance::findBestMove() {
    int middleNumber = totalSum / 2;
    pair<int, int> bestMove = { -1, -1 };
    int closestDiff = INT_MAX;
    const int threshold = 1;

    if (leftSum > rightSum) {

        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols / 2; ++j) {
                int weight = ship[i][j];

                if (weight != 0 && weight != -1) {
                    vector<pair<int, int>> path = findShortestPath(i, j);
                    if (!path.empty()) {
                        int tempRightSum = rightSum + weight;
                        int diff = abs(tempRightSum - middleNumber);

                        if (diff < closestDiff) {
                            closestDiff = diff;
                            bestMove = { i, j };
                        }
                        if (diff <= threshold) {
                            return bestMove;
                        }
                    }
                }
            }
        }
    }
    else {
        for (int i = 0; i < rows; ++i) {
            for (int j = cols / 2; j < cols; ++j) {
                int weight = ship[i][j];
                if (weight != 0 && weight != -1) {
                    vector<pair<int, int>> path = findShortestPath(i, j);
                    if (!path.empty()) {
                        int tempLeftSum = leftSum + weight;
                        int diff = abs(tempLeftSum - middleNumber);
                        if (diff < closestDiff) {
                            closestDiff = diff;
                            bestMove = { i, j };
                        }
                        if (diff <= threshold) {
                            return bestMove;
                        }
                    }
                }
            }
        }
    }
    return bestMove;
}



void Balance::printShip() {
    cout << "current ship:" << endl;
    for (int i = 0; i < ship.size(); i++) {
        for (int j = 0; j < ship[i].size(); j++) {
            cout << setw(5) << ship[i][j] << " ";
        }
        cout << endl;
    }
}
