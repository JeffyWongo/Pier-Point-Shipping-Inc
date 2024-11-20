#ifndef CONTAINER_H
#define CONTAINER_H

#include <string>
#include <vector>

using namespace std;

class Container {
    public:
        string name;
        int weight;

        Container();
        Container(string containerName, int containerWeight);
};

#endif