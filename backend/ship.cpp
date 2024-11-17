#include "ship.h"

using namespace std;


Ship::Ship(){
    vector<vector<Container>> manifest(8, vector<Container>(12));
}

void Ship::readManifest(string){

}

vector<vector<Container>>& Ship::returnManifest(){
    return manifest;
}