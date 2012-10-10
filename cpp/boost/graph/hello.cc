#include <iostream>
#include <sstream>
#include <utility>

#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>

static const int num_nodes = 4;

main()
{
    // Vertices
    enum nodes {A, B, C, D};

    // Make the graph /////////////////
    
    typedef boost::adjacency_list<boost::vecS, boost::vecS, boost::bidirectionalS> graph_t;
    graph_t g(num_nodes);

    // Fill in the graph
    boost::add_edge(A, B, g);
    boost::add_edge(B, C, g);
    boost::add_edge(A, D, g);

    // Print the graph ////////////////
    
    typedef boost::property_map<graph_t, boost::vertex_index_t>::type index_map_t;
    index_map_t index = boost::get(boost::vertex_index, g);

    typedef boost::graph_traits<graph_t>::vertex_iterator vertex_iterator_t;
    std::pair<vertex_iterator_t, vertex_iterator_t> vp;

    // Print vertices
    std::ostringstream oss;

    for(vp = boost::vertices(g) ; vp.first != vp.second ; ++vp.first) {
        oss << index[*vp.first] << " ";
    }

    std::cout << "vertices(g) = { " << oss.str() << "}" << std::endl;

    oss.str("");

    // Print edges

    boost::graph_traits<graph_t>::edge_iterator ei, ei_end;
    for(tie(ei, ei_end) = boost::edges(g) ; ei != ei_end ; ++ei) {
        oss << "(" << index[boost::source(*ei, g)] << "," << index[boost::target(*ei, g)] << ") ";
    }

    std::cout << "edges(g) = { " << oss.str() << "}" << std::endl;

}
