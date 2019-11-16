// -- Graph.cpp ---------------------------------------------------------------

#include "Graph.h"

#include <fstream>
#include <iostream>
#include <string>
#include <strstream>
#include <vector>

#include <cstdlib>  // rand(), srand()
#include <ctime>  // time() for seeding rand()

// Graph edges

Edge::Edge(unsigned u, unsigned v, int cost)
: start(u),
  end(v),
  weight(cost)
{
    // Nothing else to do.
}

Edge::~Edge()
{
    // Nothing to do.
}

// Graph object

Graph::Graph(const string& filename)
: _input_fail(false),
  _vertices(0),
  _edges(vector<Edge*>()),
  _cost(0),
  _mst_path(nullptr)
{
    // Seed the random number generator.
    srand(static_cast<unsigned>(time(0)));
    
    // Load graph data from input file name.
    ifstream in(filename);
    if(in.fail()) {
        // Input failure, d'oh.
        this->_input_fail = true;
        return;
    }

    string line;
    while(!in.eof()) {
        getline(in, line);

        // Ignore empty lines and comment lines.
        if(line.length() < 1 || line[0] == '#') {
            continue;
        }

        // Stuff the line into a string stream so we can parse it.
        istrstream instr(line.c_str());

        // If 0, we haven't seen the number of vertices yet.
        //
        // This is pretty lazy parsing that assumes your input file follows
        // the correct format. You should never do that in real code.
        if(this->_vertices == 0) {
            instr >> this->_vertices;
        } else {
            // Must be an edge definition!
            unsigned start, end;
            int weight;

            instr >> start >> end >> weight;
            Edge* e = new Edge(start, end, weight);
            this->_edges.push_back(e);
        }
    }
}

Graph::~Graph()
{
    // If we've calculated an MST, we need to clean up the path.
    if(this->_mst_path != nullptr) {
        delete _mst_path;
        _mst_path = nullptr;
    }

    // Delete the edges we created earlier.
    for(vector<Edge*>::iterator it = this->_edges.begin() ; it != this->_edges.end(); it++ ) {
        delete *it;
    }
    this->_edges.clear();
}

// Find all the edges for the given vector.
//
// Caller must delete the vector, but not its contents. Contents are still
// owned by this->_edges.
vector<Edge*>* Graph::edges_for(unsigned vertex)
{
    vector<Edge*>* edges = new vector<Edge*>;

    for(vector<Edge*>::iterator it = this->_edges.begin(); it != this->_edges.end(); it++ ) {
        if((*it)->start == vertex || (*it)->end == vertex) {
            edges->push_back(*it);
        }
    }
    
    return edges;
}

// Run Prim's algorithm over the graph to find a minimum spanning tree.
//
// Returns total cost of the MST.
int Graph::calculate_mst()
{
    // If you've called this before, just exit; we've already calculated an
    // MST. Otherwise, we'd have to delete this->_mst_path so we didn't leak.
    if(this->_mst_path != nullptr) {
        return this->_cost;
    }
    
    vector<Edge*>* tree = new vector<Edge*>;
    int cost = 0;
    vector<bool> spanned(this->_vertices);
    for(unsigned i = 0; i < this->_vertices; i++) {
        spanned[i] = false;
    }

    // Start with an arbitrary vertex.
    unsigned start_vertex = static_cast<unsigned>(rand()) % this->_vertices;
    spanned[start_vertex] = true;
    unsigned seen = 1;  // number of spanned vertices

    // Add edges until we've seen all of the vertices.
    while(seen < this->_vertices) {
        // For all edges, find the cheapest one with a vertex we've already
        // seen and the other vertex that hasn't been seen.
        Edge* best_edge = nullptr;
        for(unsigned i = 0; i < this->_vertices; i++) {
            if(spanned[i] == true) {
                vector<Edge*>* edges = this->edges_for(i);
                for(vector<Edge*>::iterator it = edges->begin(); it != edges->end(); it++) {
                    Edge* current_edge = *it;
                    if(spanned[current_edge->start] && spanned[current_edge->end]) {
                        // These vertices are both in the tree already.
                        continue;
                    }

                    if(best_edge ==  nullptr || current_edge->weight < best_edge->weight) {
                        best_edge = current_edge;
                    }
                }
                delete edges;  // Don't delete the edges, just the vector.
            }
        }
        
        if(best_edge != nullptr) {
            // Add the best edge to our MST.
            tree->push_back(best_edge);

            if(spanned[best_edge->start] == false) {
                spanned[best_edge->start] = true;
                seen++;
            } else {
                spanned[best_edge->end] = true;
                seen++;
            }

            cost += best_edge->weight;
        } else {
            // The graph isn't connected. We're not handling those. Clean up
            // and get out of here.
            delete tree;

            return(0);
        }
    }

    this->_cost = cost;
    this->_mst_path = tree;

    return this->_cost;
}
