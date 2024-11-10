#ifndef SHIP_H
#define SHIP_H

#include <string>
#include <vector>

using namespace std;

class Ship {
    private:
        vector<vector<string>> manifest;
    public:
        Ship();
        void readManifest(string);
        vector<vector<string>>& returnManifest();

};

#endif