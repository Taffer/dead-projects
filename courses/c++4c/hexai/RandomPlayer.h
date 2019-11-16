// -- RandomPlayer.h ----------------------------------------------------------
//
// A player who chooses their moves mostly randomly, but with a prefernce for
// moves along their appropriate axis.

#ifndef RANDOMPLAYER_H_
#define RANDOMPLAYER_H_

#include "hex.h"
#include "Board.h"
#include "Player.h"

class RandomPlayer: public Player {
public:
	RandomPlayer(Chits player_chit);
	virtual ~RandomPlayer();

	virtual Node* get_move(Board& hex_board);
};

#endif /* RANDOMPLAYER_H_ */
