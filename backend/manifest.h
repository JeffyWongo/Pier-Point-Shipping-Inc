#ifndef MANIFEST_H
#define MANIFEST_H

#include <string>
#include "ship.h"

using namespace std;

class Manifest{
    public:
    Manifest();
    void readManifest(const string& filename, Ship& ship);
    void outboundManifest(const string& filename, const Ship& ship);
};


#endif 