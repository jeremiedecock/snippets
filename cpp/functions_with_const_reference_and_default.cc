#include <iostream>
#include <string>

void print(const std::string & msg="Hello") {
    std::cout << msg << std::endl;
}

int main()
{
    print(); // ok

    print("Hi"); // ok

    std::string msg = "Bye";
    print(msg); // ok

    return 0;
}
