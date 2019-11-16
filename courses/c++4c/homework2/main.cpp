// A demo of Dijkstra's algorithm for the "C++ for C Programmers" course.
//
// Produces an average shortest path length for the connected paths in an
// undirected graph.
//
// 200 Words on What I Learned:
//
// For this small dataset, using the naive implementation of Dijkstra's
// algorithm (rather than an implementation using a min-heap) is "good
// enough".
//
// In a previous Coursera course, I implemented Dijkstra's using a min-heap
// and an edge list. This implementation uses an edge matrix instead so I'd
// have a chance to try the other common implementation for graph data.
//
// My version of g++, 4.7.3, is missing some "current" standard C++ bits that
// would have been helpful. For example, I wanted to use nan() and isnan()
// from <cmath>, but the implementations available to me would't work.
// Instead, I had to use 0.0 to represent "no edge" in my edge cost array.
// This is OK for our dataset, since the minimum edge cost is 1.0.
//
// I also learned that examining standard template library objects (such as
// the vectors) in Eclipse's C++ debugger is an exercise in futility. Also,
// these classes make no effort to provide operator<< methods to aid in
// debugging.
//
// Also, use queue<>'s empty() method, not its size() method, to know when
// you're done processing a queue. size() doesn't return the number of items
// currently in the queue, it returns the size of the underlying storage
// object.
//
// A sample of the program's output (one unreachable node is entirely expected
// because loops aren't allowed... the path from 0 -> 0 doesn't exist):
//
// Making a graph...
// Found 1 unreachable nodes.
// At 20% density, the average path is 5.37449
// Found 1 unreachable nodes.
// At 40% density, the average path is 3.48898

#include <cstdlib>  // For srand(), rand().
#include <ctime>  // For time().

#include <iostream>
#include <map>
#include <queue>
#include <vector>

using namespace std;

// A basic graph object. Implemented using an edge matrix because we're
// using small (50 node) graphs; this keeps the implementation simpler. If we
// were working with large graphs, the adjacency list would be a better
// choice, as our expected density is only 20% - 40%.
class Graph
{
public:
	// Create a new (empty) graph of the specified size.
	Graph(const unsigned num_nodes=5)
		: size(num_nodes),
		  costs(nullptr) {
		this->costs = new double*[this->size];  // # of rows

		for(unsigned i = 0; i < this->size; i++) {
			this->costs[i] = new double[this->size];  // # of columns

			for(unsigned j = 0; j < this->size; j++) {
				this->costs[i][j] = 0.0;  // No edge exists.
			}
		}

		// Initialize the random number generator.
		srand(time(0));
	}

	// Release the graph's memory.
	~Graph() {
		for(unsigned i = 0; i < this->size; i++) {
			delete[] this->costs[i];
		}
		delete[] this->costs;

		this->costs = nullptr;
	}

	// Return a vector of the edges connected to the given node.
	// Caller must delete the vector.
	vector<unsigned>* edges_for(unsigned node) {
		vector<unsigned>* edges = new vector<unsigned>();

		for(unsigned i = 0; i < this->size; i++) {
			if(node == i) continue;

			if(this->costs[node][i] > 0.0) {
				edges->push_back(i);
			}
		}

		return(edges);
	}

	// Return the cost of an edge between the given nodes.
	// Returns 0.0 if no edge exists.
	double get_edge(unsigned start, unsigned end) {
		return(this->costs[start][end]);
	}

	// Return a probability value 0.0 - 1.0.
	inline double probability(void) {
		return(static_cast<double>(rand() % 100) / 100.0);
	}

	// Randomly create edges in the graph using the specified density. The
	// cost for traveling on an edge is between min_cost and max_cost.
	void randomize(const double density, const double max_cost, const double min_cost=1.0) {
		double delta = max_cost - min_cost;

		// Check for the possibility of each edge. If it exists, give it a
		// random cost.
		for(unsigned i = 0; i < this->size; i++) {
			for(unsigned j = 0; j < this->size; j++ ) {
				if(i == j) continue;  // No loops allowed in this graph.

				bool is_edge = (this->probability() <= density);
				if(is_edge) {
					double cost = this->probability() * delta + min_cost;
					this->costs[i][j] = cost;
					this->costs[j][i] = cost;  // same, as graph is undirected
				}
			}
		}
	}

	// Calculate the average of the shortest paths between the first node and
	// all other nodes.
	double average_path(void) {
		vector<double>* distances = this->shortest_paths(0);

		unsigned found_paths = 0;
		double total_cost = 0.0;
		for(unsigned j = 1; j < this->size; j++) {
			if((*distances)[j] > 0.0) {
				found_paths++;
				total_cost += (*distances)[j];
			}
		}

		delete distances;

		if(found_paths < 1) return(0.0);

		return(total_cost / static_cast<double>(found_paths));
	}

	// Is start connected to end in this graph? Uses breadth-first search to
	// see if we can get from start to end successfully.
	bool is_connected(unsigned start, unsigned end) {
		bool* explored = new bool[this->size];
		for(unsigned i = 0; i < this->size; i++) explored[i] = false;

		queue<unsigned> nodes;
		nodes.push(start);

		while(nodes.empty() == false) {
			unsigned node = nodes.front();
			nodes.pop();

			if(explored[node] == true ) {
				// Been there already.
				continue;
			}

			vector<unsigned>* edges = this->edges_for(node);
			for(vector<unsigned>::iterator it = edges->begin(); it != edges->end(); it++) {
				if(explored[*it] == false) {
					nodes.push(*it);
				}

				if(*it == end) {
					delete edges;  // clean up
					delete[] explored;

					return(true);  // Found it!
				}
			}

			delete edges;
		}

		delete[] explored;
		return(false);  // didn't get it
	}

	// Calculate the shortest paths between the origin and all other nodes.
	// In the finest UNIX tradition, returns -1.0 if no path exists.
	// Returns a vector of distances, result [x] = path for (0, x).
	// Caller must delete the returned vector.
	vector<double>* shortest_paths(int origin) {
		map<const unsigned, double> distances;
		distances[origin] = 0.0;

		map<const unsigned, bool> processed;
		processed[origin] = true;

		// Preprocess nodes we can't reach.
		for(unsigned i = 0; i < this->size; i++) {
			if(this->is_connected(origin, i) == false) {
				// Can't get there from here.
				distances[i] = 0.0;
				processed[i] = true;
			}
		}
		cout << "Found " << processed.size() << " unreachable nodes." << endl;

		while(processed.size() < this->size) {
			unsigned best_end = 0;
			double best_cost = 0.0;

			for(map<const unsigned, bool>::iterator start = processed.begin(); start != processed.end(); start++) {
				for(unsigned j = 0; j < this->size; j++) {
					double edge = this->get_edge(start->first, j);
					if(processed.find(j) != processed.end() || edge == 0.0) {
						// j has already been processed, or there's no (*start, j) edge.
						continue;
					}

					double this_cost = distances[start->first] + edge;
					if(best_cost == 0.0 || this_cost < best_cost) {
						best_end = j;
						best_cost = this_cost;
					}
				}
			}

			if(best_cost == 0.0) {
				// All else disconnected.
				break;
			}

			processed[best_end] = true;
			distances[best_end] = best_cost;
		}

		vector<double>* results = new vector<double>(this->size);
		for(map<const unsigned, double>::iterator it = distances.begin(); it != distances.end(); it++) {
			(*results)[it->first] = it->second;
		}
		return(results);
	}

	// Print the graph's data to the given ostream.
	ostream& print(ostream& out) {
		out << "Graph: [" << endl;
		for(unsigned i = 0; i < this->size; i++) {
			out << "\t[";
			for(unsigned j = 0; j < this->size; j++) {
				if(this->costs[i][j] != 0.0) {
					out << i << "->" << j << " = " << this->costs[i][j] << ", ";
				}
			}
			out << " ]" << endl;
		}
		out << "]" << endl;

		return(out);
	}

private:
	const unsigned size;
	double** costs;  // 0.0 if no edge exists, else cost of that edge.

	// Private copy constructor so we don't call it accidentally.
	Graph(const Graph& copy);
};

// Override ostream's operator<< for Graph objects.
inline ostream& operator<<(ostream& out, Graph& g) {
	return(g.print(out));
}

// Program code.
int main(void) {
	cout << "Making a graph..." << endl;
	Graph g(50);  // 50 node graph

	// 20%
	g.randomize(0.2, 10.0);
	cout << "At 20% density, the average path is " << g.average_path() << endl;

	// 40%
	g.randomize(0.4, 10.0);
	cout << "At 40% density, the average path is " << g.average_path() << endl;

	return(0);
}
