// -- hex.h -------------------------------------------------------------------

#ifndef hex_hex_h
#define hex_hex_h

#include <iostream>

using namespace std;

enum class Chits {
    NONE,
    X,
    O
};

inline ostream& operator<<(ostream& out, Chits& c)
{
    switch(c) {
        case Chits::NONE:
            out << " ";
            break;
        case Chits::X:
            out << "X";
            break;
        case Chits::O:
            out << "O";
            break;
        default:
            // Impossible.
            break;
    }

    return out;
}

#endif
