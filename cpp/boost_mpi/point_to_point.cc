#include <iostream>
#include <string>

#include <boost/mpi.hpp>
#include <boost/serialization/string.hpp>

namespace mpi = boost::mpi;

/*
 * Required packages (Debian): mpi-default-bin, mpi-default-dev, libboost-mpi-dev
 *
 * Compile:
 *   mpic++ -o p2p point_to_point.cc -lboost_mpi -lboost_serialization
 *
 * Run:
 *   mpirun -np 2 p2p
 * 
 * See:
 * - https://www.boost.org/doc/libs/1_68_0/doc/html/mpi/tutorial.html
 * - https://www.boost.org/doc/libs/1_68_0/doc/html/mpi/getting_started.html
 * - https://stackoverflow.com/questions/40568713/unable-to-compile-simple-boost-mpi-example
 */

int main()
{
    mpi::environment env;
    mpi::communicator world;

    if (world.rank() == 0)
    {
        world.send(1, 0, std::string("Hello"));

        std::string msg;
        world.recv(1, 1, msg);

        std::cout << msg << "!" << std::endl;
    }
    else
    {
        std::string msg;
        world.recv(0, 0, msg);

        std::cout << msg << ", ";
        std::cout.flush();

        world.send(0, 1, std::string("world"));
    }

    return 0;
}