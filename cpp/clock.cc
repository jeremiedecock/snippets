#include <cstdio>
#include <ctime>
#include <cmath>
#include <iostream>

void do_something() {
    int n = 999999;
    int i, j;
    int freq = n-1;

    for(i=2 ; i<=n ; ++i) {
        for(j=sqrt(i) ; j>1 ; --j) {
            if(i%j == 0) {
                --freq;
                break;
            }
        }
    }
}

int main ()
{
    clock_t t1 = clock();

    std::cout << "CLOCKS_PER_SEC=" << CLOCKS_PER_SEC << std::endl << std::endl;

    std::cout << "clock t1=" << t1 << std::endl;
    std::cout << "sec t1=" << ((float) t1) / CLOCKS_PER_SEC << std::endl << std::endl;

    do_something();

    clock_t t2 = clock();

    std::cout << "clock t2=" << t2 << std::endl;
    std::cout << "sec t2=" << ((float) t2) / CLOCKS_PER_SEC << std::endl << std::endl;

    clock_t t3 = t2 - t1;

    std::cout << "deltatime=" << ((float)t3) / CLOCKS_PER_SEC << std::endl;

    return 0;
}
