#include <iostream>
#include <map>
#include <vector>

/*
 * See:
 * - https://en.wikipedia.org/wiki/C%2B%2B11#Range-based_for_loop
 * - https://en.wikipedia.org/wiki/C%2B%2B11#Type_inference
 * - https://en.cppreference.com/w/cpp/language/range-for
 */

main() {
    const int N = 5;
    int a[N] = {1, 2, 3, 4, 5};

    std::vector<int> v = {1, 2, 3, 4, 5};
    
    std::map<std::string, int> m = {{std::string("one"), 1},
                                    {std::string("two"), 2},
                                    {std::string("three"), 3}};

    // "classic" loop /////////////////////////////////////////////////////////

    for(int i = 0 ; i < N ; i++) {
        std::cout << a[i] << " ";
    }
    std::cout << std::endl;

    for(std::vector<int>::iterator it = v.begin() ; it != v.end() ; it++) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;

    for(std::map<std::string, int>::iterator it = m.begin() ; it != m.end() ; it++) {
        std::cout << it->first << ":" << it->second << " ";
    }
    std::cout << std::endl;

    // Range-based for loop ///////////////////////////////////////////////////
    
    for(int & x : a) {
        std::cout << x << " ";
    }
    std::cout << std::endl;

    for(int & x : v) {
        std::cout << x << " ";
    }
    std::cout << std::endl;

    for(std::pair<const std::string, int> & x : m) {
        std::cout << x.first << ":" << x.second << " ";
    }
    std::cout << std::endl;

    // Range-based for loop and type inference ////////////////////////////////

    for(auto & x : a) {
        std::cout << x << " ";
    }
    std::cout << std::endl;

    for(auto & x : v) {
        std::cout << x << " ";
    }
    std::cout << std::endl;

    for(auto & x : m) {
        std::cout << x.first << ":" << x.second << " ";
    }
    std::cout << std::endl;
}