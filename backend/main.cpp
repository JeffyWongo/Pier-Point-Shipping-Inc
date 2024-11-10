#include <iostream>
#include <string>
#include "loading.h"
#include "ship.h"

using namespace std;

void loadOperation();

int main(){
    loadOperation();
}

void loadOperation(){
    Ship ship = Ship();
    Loading::load(ship);
}

