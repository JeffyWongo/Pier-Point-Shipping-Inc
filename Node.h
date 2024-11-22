#pragma once
// Node.h
#ifndef NODE_H
#define NODE_H

#include <vector>
using namespace std;

struct Node {
    int row, col;
    int g, h; // g: cost, h: heuristic
    vector<pair<int, int>> path; // to store the route

    int f() const { return g + h; }
    bool operator>(const Node& other) const { return f() > other.f(); }
};

#endif
