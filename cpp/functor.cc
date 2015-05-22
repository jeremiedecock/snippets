#include <iostream>

class AffineFunction
{
    public:
        double a, b;

    public:
        AffineFunction(double _a, double _b) {
            this->a = _a;
            this->b = _b;
        }

        double operator() (double x) {
            return this->a * x + this->b;
        }
};

int main()
{
    AffineFunction f(2., 3.);

    for(double x=0 ; x<10. ; x++) {
        std::cout << f(x) << std::endl;
    }

    return 0;
}

