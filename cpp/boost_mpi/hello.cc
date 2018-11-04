#include <boost/mpi/environment.hpp>
#include <boost/mpi/communicator.hpp>

namespace mpi = boost::mpi;

/*
 * Required packages (Debian): mpi-default-bin, mpi-default-dev, libboost-mpi-dev
 *
 * Compile:
 *   mpic++ -o hello hello.cc -lboost_mpi
 *
 * Run:
 *   mpirun -np 4 hello
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

    std::cout << "I am process " << world.rank() << " of " << world.size() << "." << std::endl;
    
    return 0;
}