// -- Player.h ----------------------------------------------------------------
//
// Abstract base class for AI Players.

#ifndef PLAYER_H_
#define PLAYER_H_

#include "Board.h"

class Player {
public:
	Player(Chits player_chit) :
		_chit(player_chit) {};
	virtual ~Player() {};

	virtual Node* get_move(Board& hex_board) = 0;

private:
	Player();
	Player(const Player& p);

protected:
	Chits _chit;
};

#endif /* PLAYER_H_ */
