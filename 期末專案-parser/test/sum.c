#include <stdio.h>

#define abc(a,b) \
    (a + b)

int main(void)
{
    int result = abc(3, 4);
    printf("Result: %d\n", result);
    return 0;
}