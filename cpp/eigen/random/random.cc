/*
 * A very basic demo of libeigen3.
 *
 * USAGE:
 *    g++ -o random -I /PATH/TO/EIGEN/ random.cc
 * or
 *    g++ -o random $(pkg-config --cflags eigen3) random.cc
 */

#include <cstdlib>
#include <ctime>
#include <iostream>

#include <Eigen/Dense>

using namespace Eigen;

int main()
{
    // Initialize the pseudo-random number generator (Eigen uses rand() internally).
    srand(time(0));

    MatrixXd m1 = MatrixXd::Random(3, 3);
    Matrix3d m2 = Matrix3d::Random();

    std::cout << m1 << std::endl;
    std::cout << m2 << std::endl;
}
