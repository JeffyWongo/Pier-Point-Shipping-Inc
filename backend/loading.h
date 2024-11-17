#ifndef LOADING_H
#define LOADING_H

#include <string>
#include <vector>
#include "ship.h"

using namespace std;

class Loading {
    private:
        static void unloading();
        static void loading();
    public:
        static void load(Ship&);

};

#endif