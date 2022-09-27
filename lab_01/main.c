#include "license.h"

int main() 
{
    if (!cmp_key()) {
        printf("Success.\n");
    }
    else {
        printf("Fail.\n");
    }
    return EXIT_SUCCESS;
}