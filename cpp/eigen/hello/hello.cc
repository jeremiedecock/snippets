/*
 * A very basic demo of libeigen3.
 *
 * USAGE:
 *    g++ -o hello -I /PATH/TO/EIGEN/ hello.cc
 * or
 *    g++ -o hello $(pkg-config --cflags eigen3) hello.cc
 */

#include <iostream>
#include <Eigen/Dense>

int main()
{
    /*
     * Buid a matrix
     */

    Eigen::Matrix<double, 2, 2> m; // <=> Matrix2d

    m(0,0) = 4;
    m(1,0) = 3.14;
    m(0,1) = -8;
    m(1,1) = m(1,0) + m(0,1);

    std::cout << std::endl << "Matrix:" << std::endl << m << std::endl;

    /*
     * Buid an array
     */

    Eigen::Array<double, 2, 2> a; // <=> Array22d

    a(0,0) = 4;
    a(1,0) = 3.14;
    a(0,1) = -8;
    a(1,1) = a(1,0) + a(0,1);

    std::cout << std::endl << "Array:" << std::endl << a << std::endl;

    /*
     * Buid a vector
     */

    Eigen::Matrix<double, 2, 1> v; // <=> Vector2d

    v(0,0) = 4;
    v(1,0) = 3.14;

    std::cout << std::endl << "Vector:" <<  std::endl << v << std::endl;
}
