#include <stdio.h>
#include "include/calculator.h"


int main() {
    int x = 10;
    int y = 5;
    int result = multiply(x, y);

    printf("--- Hello from the Unix Engine ---\n");
    printf("The result of %d * %d is: %d\n", x, y, result);
    printf("Compilation and Linking Successful!\n");
    
    return 0;
}
