// -- LongPathPlayer.h --------------------------------------------------------
//
// An AI player who attempts to make their longest path longers.

#ifndef LONGPATHPLAYER_H_
#define LONGPATHPLAYER_H_

#include "hex.h"
#include "Board.h"
#include "Player.h"

class LongPathPlayer: public Player {
public:
	LongPathPlayer(Chits player_chit);
	virtual ~LongPathPlayer();

	virtual Node* get_move(Board& hex_board);

private:
	bool _moves_northsouth;  // False for X, True for O.

	Node& choose_closest(Node& one, Node& two, unsigned size);
};

#endif /* LONGPATHPLAYER_H_ */
