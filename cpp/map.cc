#include <map>
#include <string>
#include <iostream>

main() {
    std::map<std::string, int> m;

    m[std::string("un")] = 1;
    m[std::string("deux")] = 2;
    m[std::string("foo")] = 11;

    std::map<std::string, int>::iterator it;

    it = m.find(std::string("foo")); 

    if(it != m.end()) {
        std::cout << it->first << std::endl;
        std::cout << it->second << std::endl;
    }
}
