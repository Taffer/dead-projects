// -- RandomPlayer.cpp --------------------------------------------------------

#include "RandomPlayer.h"

#include <cstdlib>

RandomPlayer::RandomPlayer(Chits player_chit)
	: Player(player_chit)
{
	// Initialize random number generator.
	srand(static_cast<unsigned>(time(nullptr)));
}

RandomPlayer::~RandomPlayer()
{
}

// Random Player behaviour:
//
// On first move, choose random unclaimed spot.
//
// On subsequent moves, flip a coin:
// - if heads, choose random unclaimed spot
// - if tails, choose random claimed spot, move on unclaimed neighbour
Node* RandomPlayer::get_move(Board& hex_board)
{
	bool flip = rand() % 2 == 1;

	vector<Node>* positions = hex_board.played_locations(this->_chit);
	if(flip || positions->size() == 0) {
		// Got 'heads' on the flip, or first move, choose randomly.
		unsigned x = 0;
		unsigned y = 0;
		do {
			x = rand() % hex_board.size();
			y = rand() % hex_board.size();
		} while(!hex_board.is_legal(x, y) );

		Node* move = new Node(x, y);
		return(move);
	}

	// Choose a random position and move near it.
	Node* move = nullptr;
	do {
		unsigned index = rand() % static_cast<unsigned>(positions->size());
		Node& start = positions->at(index);
		vector<Node>* neighbours = hex_board.neighbours_for(start.first, start.second);
		vector<Node>* possible = new vector<Node>;
		for(auto it = neighbours->begin(); it != neighbours->end(); it++) {
			// You could improve this move by preferring positions in the correct
			// axis for each player; East-West for X, North-South for O. This
			// Player isn't smart.
			if(hex_board.is_legal((*it).first, (*it).second)) {
				possible->push_back(*it);
			}
		}

		if(possible->size() == 0) {
			// Nope, try again. Note that this could infinitely loop if you
			// got very unlucky on a mostly-full board.
			delete possible;
			delete neighbours;
			continue;
		}

		index = rand() % static_cast<unsigned>(possible->size());
		Node& target = possible->at(index);
		move = new Node(target.first, target.second);
		delete possible;
		delete neighbours;
	} while(move == nullptr);

	return(move);
}
