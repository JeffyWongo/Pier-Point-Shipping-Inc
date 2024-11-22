// Balance.cpp
#include "Balance.h"
#include <iostream>
#include <queue>
#include <unordered_map>
#include <cmath>
#include <string>

using namespace std;

Balance::Balance(vector<vector<int>>& initialShip) : ship(initialShip) {}

int Balance::calculateHeuristic(int row, int col, bool moveToRight) { // doesn't really need row tho, but keep it to keep everything clear
    if (moveToRight) {
        return abs(col - 6); // how long still need to get to the right
    }
    else {
        return abs(col - 5); // how long still need to get to the left
    }
}

vector<pair<int, int>> Balance::findShortestPath(int startRow, int startCol) {
    priority_queue<Node, vector<Node>, greater<Node>> openList; // use this so smallest h() value is at the very front
    unordered_map<string, bool> visited;
    vector<pair<int, int>> directions = { {-1, 0}, {1, 0}, {0, -1}, {0, 1} }; // possible directions

    // determine if the element if moving to left to moving to right
    bool moveToRight = (startCol < 6); // if less than 6, then it's on the left so moving to right

    // push the startNode to the openList
    Node startNode = { startRow, startCol, 0, calculateHeuristic(startRow, startCol, moveToRight), {} }; //row, col, g, h, path
    openList.push(startNode);

    while (!openList.empty()) {
        Node current = openList.top();
        openList.pop(); // check the first node

        // see if it's in the goal state
        if ((moveToRight && current.col >= 6 && ship[current.row][current.col] == 0) || // this means the goal is move to right and it's already on the right half
            (!moveToRight && current.col < 6 && ship[current.row][current.col] == 0)) { // this means the goal is move to left and it's already on the left half
            return current.path;
        }

        // mark the visited point, if already marked then skip it
        string state = to_string(current.row) + "-" + to_string(current.col); // ex:3-2
        if (visited[state]) continue;
        visited[state] = true;

        // check possible dir and explore
        for (auto& dir : directions) {
            int newRow = current.row + dir.first;
            int newCol = current.col + dir.second;

            // check possible obstacles
            if (newRow < 0 || newRow >= 8 || newCol < 0 || newCol >= 12) continue; // can't go beyond the ship
            if (visited[to_string(newRow) + "-" + to_string(newCol)]) continue; // can't go back
            if (ship[newRow][newCol] != 0) continue; // can't go through a existed node

            // cal for new h
            int newG = current.g + 1;
            int newH = calculateHeuristic(newRow, newCol, moveToRight);

            // add new note to openList
            Node newNode = { newRow, newCol, newG, newH, current.path };
            newNode.path.push_back({ newRow, newCol });
            openList.push(newNode);
        }
    }

    return {}; // if fail to find a route
}

void Balance::printShip() {
    cout << "current ship：" << endl;
    for (int i = 0; i < ship.size(); i++) {
        for (int j = 0; j < ship[i].size(); j++) {
            cout << ship[i][j] << " ";
        }
        cout << endl;
    }
}
