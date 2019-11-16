// -- main.cpp ----------------------------------------------------------------

#include <fstream>
#include <iostream>

#include "Graph.h"

using namespace std;

int main(int argc, const char* argv[])
{
    // Handle multiple files from the command-line. Handy for testing!
    for(int i = 1; i < argc; i++) {
        Graph g(argv[i]);
        if(g.fail() == true) {
            cout << "Unable to load graph data from " << argv[i] << "." << endl;
            continue;
        }

        int cost = g.calculate_mst();
        const vector<Edge*>* path = g.get_mst_edges();
        if(path == nullptr) {
            cout << "Failed to calculate an MST for the graph." << endl;
            continue;
        }

        cout << "In " << argv[i] << ", the MST costs " << cost << "." << endl;
        cout << "Path:" << endl;
        for(vector<Edge*>::const_iterator it = path->cbegin(); it != path->cend(); it++ ) {
            cout << "\t" << (*it)->start << " -> " << (*it)->end << " (" << (*it)->weight << ")" << endl;
        }
    }

    return(0);
}
