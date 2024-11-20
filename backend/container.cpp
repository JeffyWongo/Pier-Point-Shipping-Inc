#include "container.h"

Container::Container(){
    Container("UNUSED", 0);
}

Container::Container(string containerName, int containerWeight = 0){
    name = containerName;
    weight = containerWeight;
}
