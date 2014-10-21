#include <iostream>

int main() {
#pragma omp parallel
    std::cout << "Hello world" << std::endl;
    return 0;
}
