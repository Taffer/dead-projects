// -- LongPathPlayer.cpp ------------------------------------------------------

#include "LongPathPlayer.h"

#include <cstdlib>

LongPathPlayer::LongPathPlayer(Chits player_chit)
	: Player(player_chit),
	  _moves_northsouth(player_chit == Chits::O)
{
	// Initialize random number generator. Not used a whole lot in this Player.
	srand(static_cast<unsigned>(time(nullptr)));
}

LongPathPlayer::~LongPathPlayer()
{
}

// Long Path Player behaviour:
//
// On first move, choose a centre square.
//
// On subsequent moves:
// - choose existing position closest to preferred edges
// - choose neighbour closest to preferred edges (North-South for O, East-West
//   for X)
// - if neighbours full, chose an new existing position and try again
// - if all existing positions exhausted, choose random position as fallback
Node* LongPathPlayer::get_move(Board& hex_board)
{
	vector<Node>* positions = hex_board.played_locations(this->_chit);
	if(positions->size() == 0) {
		// First move!
		unsigned x = hex_board.size() / 2;
		unsigned y = hex_board.size() / 2;
		while(!hex_board.is_legal(x, y)) {
			// Coin flip to break ties.
			bool flip = rand() % 2 == 1;
			if(_moves_northsouth) {
				if(flip) {
					x++;
				} else {
					x--;
				}
			} else {
				if(flip) {
					y++;
				} else {
					y--;
				}
			}
		}
		return(new Node(x, y));
	}

	// From existing positions, choose one that's close to an edge, but not
	// up against an edge.
	Node *move = nullptr;
	while(move == nullptr) {
		// Exhaustive search through all occupied positions' neighbours.  This
		// is O(n) because each node has a constant number of neighbours.
		vector<Node> potential_moves;
		for(auto it = positions->begin(); it != positions->end(); it++) {
			vector<Node>* neighbours = hex_board.neighbours_for((*it).first, (*it).second);
			for(auto n = neighbours->begin(); n != neighbours->end(); n++) {
				if(hex_board.is_legal(n->first, n->second)) {
					// This will lead to duplicate potential moves.
					potential_moves.push_back((*n));
				}
			}
			delete neighbours;
		}

		if(potential_moves.size() < 1) {
			// Nothing suitable, pick randomly as a fallback.
			unsigned x = rand() % hex_board.size();
			unsigned y = rand() % hex_board.size();
			while(!hex_board.is_legal(x, y)) {
				x = rand() % hex_board.size();
				y = rand() % hex_board.size();
			}
			move = new Node(x, y);
		} else {
			Node& best = potential_moves.at(0);
			for(auto potential = potential_moves.begin(); potential != potential_moves.end(); potential++) {
				best = choose_closest(best, *potential, hex_board.size());
			}
			move = new Node(best.first, best.second);
		}
	}
	delete positions;

	return(move);
}

// Choose the node closest to this player's preferred edges.
Node& LongPathPlayer::choose_closest(Node& one, Node& two, unsigned size)
{
	unsigned mid = size / 2;
	if(_moves_northsouth) {
		if(one.second <= mid && two.second <= mid) {  // both closer to 0
			return((one.second < two.second) ? one : two);
		}

		if(one.second > mid && two.second > mid) {  // both closer to size
			return((one.second > two.second) ? one : two);
		}

		// Mixed results, pick the one closest to its edge.
		unsigned dy_one = (one.second <= mid) ? one.second : size - one.second;
		unsigned dy_two = (two.second <= mid) ? two.second : size - two.second;

		return((dy_one < dy_two) ? one : two);
	} else {
		if(one.first <= mid && two.first <= mid) {  // both closer to 0
			return((one.first < two.first) ? one : two);
		}

		if(one.first > mid && two.first > mid) {  // both closer to size
			return((one.first > two.first) ? one : two);
		}

		// Mixed results, pick the one closest to its edge.
		unsigned dx_one = (one.first <= mid) ? one.first : size - one.first;
		unsigned dx_two = (two.first <= mid) ? two.first : size - two.first;

		return((dx_one < dx_two) ? one : two);
	}
}
