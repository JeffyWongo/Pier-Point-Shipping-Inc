#ifndef SHIP_H
#define SHIP_H

#include <string>
#include <vector>
#include "container.h"

using namespace std;

class Ship {
    private:
        vector<vector<Container>> manifest;
    public:
        Ship();
        void readManifest(string);
        vector<vector<Container>>& returnManifest();

};

#endif