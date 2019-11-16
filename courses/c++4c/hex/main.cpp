// -- main.cpp ----------------------------------------------------------------
//
// Hex game

#include "Board.h"

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
        } else {
            cout << "Player 'O', ";
        }

        unsigned x = size + 1;
        cout << "enter your X co-ordinate (1 - " << size << "): ";
        if(!(cin >> x) || x == 0 || x > size) {
            cout << "Invalid input, try again." << endl;
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            continue;
        }

        unsigned y = size + 1;
        cout << "Enter your Y co-ordinate (1 - " << size << "): ";
        if(!(cin >> y) || x == 0 || x > size) {
            cout << "Invalid input, try again." << endl;
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            continue;
        }

        // Player enters co-ordinates in 1 - size, but we operate in 0 -
        // (size - 1).
        x--;
        y--;
        
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
