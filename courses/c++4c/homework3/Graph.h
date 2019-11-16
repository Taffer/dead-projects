// -- Graph.h -----------------------------------------------------------------

#ifndef homework3_Graph_h
#define homework3_Graph_h

#include <string>
#include <vector>

using namespace std;

// An edge in the graph.
class Edge {
public:
    Edge(unsigned start, unsigned end, int weight);  // Create an edge.
    virtual ~Edge();  // Gozer, the desctructor.

    const unsigned start;  // Starting vertex of this edge.
    const unsigned end;  // Ending vertext of this edge.
    const int weight;  // Weight on this edge. Can be negative, we don't mind.

private:
    Edge();  // default constructor
    Edge(const Edge& e);  // copy constructor
};

// An undirected graph object that knows how to find its minimum spanning
// tree (MST) using Prim's algorithm.
class Graph {
public:
    Graph(const string& filename);  // Read Graph data from file.
    virtual ~Graph();  // destructor

    inline bool fail() {  // Failed to read data from input file.
        return this->_input_fail;
    };

    int calculate_mst();  // Calculate the MST and return its cost.

    // Graph owns this pointer, not the caller; don't delete it.
    // Returns nullptr if you haven't calculated an MST yet.
    inline const vector<Edge*>* get_mst_edges() {  // Get the edges in the MST.
        return this->_mst_path;
    }

    vector<Edge*>* edges_for(unsigned vertex);  // Get all edges for a vertex.
    
private:
    Graph();  // default constructor
    Graph(const Graph& g);  // copy constructor

    bool _input_fail;  // True when we couldn't read the input file.

    unsigned _vertices;  // Number of vertices.
    vector<Edge*> _edges;  // Edges in the graph.

    int _cost;  // MST's cost; 0 when not calculated.
    vector<Edge*>* _mst_path;  // MST edges; nullptr when not calculated.
};

#endif
