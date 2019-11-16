// -- Board.h -----------------------------------------------------------------
//
// Hex board class

#ifndef __hex__Board__
#define __hex__Board__

#include "hex.h"

#include <iostream>
#include <utility>
#include <vector>

using namespace std;

typedef pair<unsigned, unsigned> Node;

// A board for the game of Hex.
class Board {
public:
    Board(unsigned size);  // Create a hex board with size x size positions.
    virtual ~Board();  // Destructor.

    // What neighbours exist for this position in the board?
    vector<Node>* neighbours_for(unsigned x, unsigned y);
    
    // Is a move to this position legal for the given player?
    bool is_legal(unsigned x, unsigned y);

    // Has the given player won?
    bool is_won(Chits who);

    // Make a move at the given position. Assumes you've called is_legal()
    // before attempting to move().
    void move(unsigned x, unsigned y, Chits who);

    // Display the board as ASCII art.
    friend ostream& operator<<(ostream& out, Board& b);

private:
    Board();  // No default constructor for you!
    Board(const Board& b);  // No copy constructor for you!

    unsigned _size;  // Width/height of the rhombus board.
    Chits** _chits;  // Whose cits are on each node?
};

#endif /* defined(__hex__Board__) */
