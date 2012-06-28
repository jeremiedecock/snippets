/*
 * A very basic demo of libeigen3.
 *
 * USAGE:
 *    g++ -o transpose -I /PATH/TO/EIGEN/ transpose.cc
 * or
 *    g++ -o transpose $(pkg-config --cflags eigen3) transpose.cc
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

    MatrixXd a = MatrixXd::Random(3, 2);

    std::cout << std::endl << "Here is the matrix a"   << std::endl << a             << std::endl;
    std::cout << std::endl << "Here is the matrix a^T" << std::endl << a.transpose() << std::endl;
    std::cout << std::endl;

    /*
     * !! WARNING !!
     * As for basic arithmetic operators, transpose() and adjoint() simply
     * return a proxy object without doing the actual transposition.
     * If you do b = a.transpose(), then the transpose is evaluated at the same
     * time as the result is written into b. However, there is a complication
     * here.
     * If you do a = a.transpose(), then Eigen starts writing the result into a
     * before the evaluation of the transpose is finished. Therefore, the
     * instruction a = a.transpose() does not replace a with its transpose, as
     * one would expect:
     */

    //a = a.transpose(); // ERROR !!! do NOT do this, even with a square matrix !!!
}
