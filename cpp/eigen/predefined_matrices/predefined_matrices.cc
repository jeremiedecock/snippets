/*
 * A very basic demo of libeigen3.
 *
 * USAGE:
 *    g++ -o predefined_matrices -I /PATH/TO/EIGEN/ predefined_matrices.cc
 * or
 *    g++ -o predefined_matrices $(pkg-config --cflags eigen3) predefined_matrices.cc
 */

#include <iostream>
#include <Eigen/Dense>

using namespace Eigen;

int size = 3;
int low = 1;
int high = 3;

int main()
{
    /*
     * Using matrix template
     */
    {
        Matrix<double, 2, 3> m1 = Matrix<double, 2, 3>::Zero();
        Matrix<double, 2, 3> m2 = Matrix<double, 2, 3>::Ones();
        Matrix<double, 2, 3> m3 = Matrix<double, 2, 3>::Constant(3);
        Matrix<double, 2, 3> m4 = Matrix<double, 2, 3>::Random();
        Matrix<double, 1, 3> m5 = Matrix<double, 1, 3>::LinSpaced(size, low, high);
        Matrix<double, 3, 3> m6 = Matrix<double, 3, 3>::Identity();

        std::cout << std::endl << "Matrix<double, 2, 3>::Zero()" << std::endl << m1 << std::endl;
        std::cout << std::endl << "Matrix<double, 2, 3>::Ones();" << std::endl << m2 << std::endl;
        std::cout << std::endl << "Matrix<double, 2, 3>::Constant(3)" << std::endl << m3 << std::endl;
        std::cout << std::endl << "Matrix<double, 2, 3>::Random()" << std::endl << m4 << std::endl;
        std::cout << std::endl << "Matrix<double, 2, 3>::LinSpaced(size, low, high)" << std::endl << m5 << std::endl;
        std::cout << std::endl << "Matrix<double, 3, 3>::Identity()" << std::endl << m6 << std::endl;
    }

    /*
     * Using typedef matrices
     */
    {
        Matrix3d m1 = Matrix3d::Zero();
        Matrix3d m2 = Matrix3d::Ones();
        Matrix3d m3 = Matrix3d::Constant(3);
        Matrix3d m4 = Matrix3d::Random();
        Matrix3d m6 = Matrix3d::Identity();

        std::cout << std::endl << "Matrix3d::Zero()" << std::endl << m1 << std::endl;
        std::cout << std::endl << "Matrix3d::Ones();" << std::endl << m2 << std::endl;
        std::cout << std::endl << "Matrix3d::Constant(3)" << std::endl << m3 << std::endl;
        std::cout << std::endl << "Matrix3d::Random()" << std::endl << m4 << std::endl;
        std::cout << std::endl << "Matrix3d::Identity()" << std::endl << m6 << std::endl;
    }

    /*
     * Using dynamic matrices
     */
    {
        MatrixXd m1 = MatrixXd::Zero(2, 3);
        MatrixXd m2 = MatrixXd::Ones(2, 3);
        MatrixXd m3 = MatrixXd::Constant(2, 3, 9);
        MatrixXd m4 = MatrixXd::Random(2, 3);
        MatrixXd m6 = MatrixXd::Identity(3, 3);

        std::cout << std::endl << "MatrixXd::Zero(2, 3)" << std::endl << m1 << std::endl;
        std::cout << std::endl << "MatrixXd::Ones(2, 3);" << std::endl << m2 << std::endl;
        std::cout << std::endl << "MatrixXd::Constant(2, 3, 9)" << std::endl << m3 << std::endl;
        std::cout << std::endl << "MatrixXd::Random(2, 3)" << std::endl << m4 << std::endl;
        std::cout << std::endl << "MatrixXd::Identity(3, 3)" << std::endl << m6 << std::endl;
    }

    /*
     * Using dynamic vectors
     */
    {
        VectorXd m1 = VectorXd::Zero(3);
        VectorXd m2 = VectorXd::Ones(3);
        VectorXd m3 = VectorXd::Constant(3, 9);
        VectorXd m4 = VectorXd::Random(3);
        VectorXd m5 = VectorXd::LinSpaced(size, low, high);

        std::cout << std::endl << "VectorXd::Zero(3)" << std::endl << m1 << std::endl;
        std::cout << std::endl << "VectorXd::Ones(3);" << std::endl << m2 << std::endl;
        std::cout << std::endl << "VectorXd::Constant(3, 9)" << std::endl << m3 << std::endl;
        std::cout << std::endl << "VectorXd::Random(3)" << std::endl << m4 << std::endl;
        std::cout << std::endl << "VectorXd::LinSpaced(size, low, high)" << std::endl << m5 << std::endl;
    }
}
