#include <iostream>
#include <vector>

class Foo {
    private:
        std::vector<int> vec;

    public:

        Foo(std::vector<int> _vec) : vec(_vec) { }

        std::vector<int> getVector() {
            return this->vec;
        }
};


main() {
    std::vector<int> vec1;
    vec1.push_back(1);
    vec1.push_back(2);
    vec1.push_back(3);

    Foo foo(vec1);

    //// WRONG!!!
    //// "foo.getVector().begin()" and "foo.getVector().end()" return 2 different objects !!!
    //std::vector<int>::iterator it;
    //for(it = foo.getVector().begin() ; it != foo.getVector().end() ; it++) {
    //    std::cout << (*it) << std::endl;
    //}
    
    // OK
    std::vector<int>::iterator it;
    std::vector<int> vec2 = foo.getVector();
    for(it = vec2.begin() ; it != vec2.end() ; it++) {
        std::cout << (*it) << std::endl;
    }

}

