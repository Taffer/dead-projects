// -- main.cpp ----------------------------------------------------------------
//
// Hex game

#include "Board.h"
#include "LongPathPlayer.h"
#include "RandomPlayer.h"

#include <cstdlib>
#include <iostream>
#include <limits>

using namespace std;

int main(int argc, const char * argv[])
{
    if(argc < 2) {
        cout << "Usage: " << argv[0] << " size" << endl;
        cout << "\tWhere size is the board size." << endl;
        return(-1);
    }
    unsigned size = static_cast<unsigned>(atoi(argv[1]));
    // 13 because that's all that will fit on an 80-character terminal.
    if(size < 3 || size > 13) {
        cout << "Size must be between 3 and 13." << endl;
        return(-1);
    }

    // AI Players
    Player *player_x = new RandomPlayer(Chits::X);
    Player *player_o = new LongPathPlayer(Chits::O);
    Player *current_player = nullptr;

    // Game's main loop.
    Board hexgame(size);
    Chits winner = Chits::NONE;
    unsigned moves = 0;
    while(winner == Chits::NONE) {
        cout << "Board:" << endl;
        cout << hexgame << endl;

        Chits player = (moves % 2 == 0) ? Chits::X : Chits::O;
        if(player == Chits::X) {
            cout << "Player 'X', ";
            current_player = player_x;
        } else {
            cout << "Player 'O', ";
            current_player = player_o;
        }

        pair<unsigned, unsigned> *move = current_player->get_move(hexgame);
        unsigned x = move->first;
        unsigned y = move->second;
        delete move;

        // Need to add 1 for display purposes.
        cout << "chooses (" << (x + 1) << ", " << (y + 1) << ")" << endl;

        // With AI players, is_legal() should always be true.
        if(hexgame.is_legal(x, y)) {
            hexgame.move(x, y, player);
            moves++;
            if(hexgame.is_won(player)) {
                winner = player;
            }
        }
    }

    cout << endl;
    cout << hexgame << endl;
    cout << "Congratulations Player ";
    if(winner == Chits::X) {
        cout << "'X'";
    } else {
        cout << "'O'";
    }
    cout << "!" << endl;
    
    return(0);
}
