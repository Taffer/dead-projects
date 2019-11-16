// -- Board.cpp ---------------------------------------------------------------
//
// Hex board class
//
// The board is a rhombus similar to the 11 x 11 board shown here:
//
// http://en.wikipedia.org/wiki/Hex_(board_game)

#include "Board.h"

#include <queue>

// Set up an initial, unplayed board with the given size.
Board::Board(unsigned size)
: _size(size),
  _chits(nullptr)
{
    // Initialize our played nodes.
    _chits = new Chits*[size];
    for(unsigned i = 0; i < size; i++) {
        _chits[i] = new Chits[size];
        for(unsigned j = 0; j < size; j++) {
            _chits[i][j] = Chits::NONE;
        }
    }
}

// Destroy a board cleanly.
Board::~Board()
{
    for(unsigned i = 0; i < _size; i++) {
        delete[] _chits[i];
    }

    delete[] _chits;
    _chits = nullptr;
}

// Return a vector of the specified grid's neighbours.
//
// Caller must delete.
vector<Node>* Board::neighbours_for(unsigned x, unsigned y)
{
    vector<Node>* neighbours = new vector<Node>;

    // Each hex can have six neighbours (XY is the current hex):
    //
    //   top-left, top-right
    // left      XY       right
    //   bot-left, bot-right
    //
    // We need to check each potential neightbour for underflow/overflow
    // before claiming they exist.  X or Y under 0 would be an underflow,
    // X or Y >= _size would be overflow.
    unsigned overflow = _size - 1;

    if(y > 0) neighbours->push_back(Node(x, y - 1));  // top-left
    if(x < overflow && y > 0) neighbours->push_back(Node(x + 1, y - 1));  // top-right
    if(x > 0) neighbours->push_back(Node(x - 1, y));  // left
    if(x < overflow)neighbours->push_back(Node(x + 1, y));  // right
    if(x > 0 && y < overflow)neighbours->push_back(Node(x - 1, y + 1)); // bottom-left
    if(y < overflow) neighbours->push_back(Node(x, y + 1)); // bottom-right

    return neighbours;
}

inline void print_indent(ostream& out, unsigned indent)
{
    for(unsigned i = 0; i < indent; i++) {
        out << " ";
    }
}

inline void print_line(ostream& out, unsigned count, unsigned indent, Chits** pieces, unsigned row)
{
    print_indent(out, indent);
    for(unsigned i = 0; i < count; i++) {
        out << "\\_/" << pieces[i][row];
    }
    out << "\\" << endl;
}

// Display the board as ASCII art.
ostream& operator<<(ostream& out, Board& b)
{
    /* X starts on this side ->
     O   _   _   _   _
     |  / \_/ \_/ \_/ \_
     v  \_/ \_/ \_/ \_/ \_
          \_/ \_/ \_/ \_/ \
            \_/ \_/ \_/ \_/
     */
    // First line.
    for(unsigned x = 0; x < b._size; x++) {
        out << " _  ";
    }
    out << endl;
    for(unsigned x = 0; x < b._size; x++) {
        out << "/" << b._chits[x][0] << "\\_";
    }
    out << endl;
    print_line(out, b._size, 0, b._chits, 1);
    
    // lines 1 - (b._size - 1)
    for(unsigned y = 1; y < b._size - 1; y++) {
        print_line(out, b._size, y * 2, b._chits, y + 1);
    }

    // Last line.
    print_indent(out, b._size * 2 - 2);
    for(unsigned x = 0; x < b._size; x++) {
        out << "\\_/ ";
    }
    out << endl;
    return out;
}

// Is a move to this position legal for the given player?
bool Board::is_legal(unsigned x, unsigned y)
{
    if(_chits[x][y] == Chits::NONE) {
        // Nobody's chosen this one.
        return true;
    }

    return false;
}

// Has the given player won?
bool Board::is_won(Chits who)
{
    // Do a BFS on the graph to see if we can travel from one side to the other.
    //
    // We could check this cheaper in move() if we noticed when a move touches
    // the player's opposite side. Then we could skip the graph search, but
    // that's not really the point of this exercise...
    bool** visited = new bool*[_size];
    for(unsigned x = 0; x < _size; x++) {
        visited[x] = new bool[_size];
        for(unsigned y = 0; y < _size; y++) {
            visited[x][y] = false;
        }
    }
    
    queue<Node> to_check;
    if(who == Chits::X) {
        // Check from top row down.
        for(unsigned x = 0; x < _size; x++) {
            to_check.push(Node(x, 0));
        }
    }
    if(who == Chits::O) {
        // Check from left column across.
        for(unsigned y = 0; y < _size; y++) {
            to_check.push(Node(0, y));
        }
    }

    bool win = false;
    while(!to_check.empty()) {
        Node node = to_check.front();
        to_check.pop();
        visited[node.first][node.second] = true;

        // Did we get to the edge? X must reach the bottom, O must reach the
        // left side.
        if((who == Chits::X && node.second == (_size - 1)) ||
           (who == Chits::O && node.first == (_size - 1))) {
            win = true;
            break;
        }

        auto neighbours = neighbours_for(node.first, node.second);
        for(auto it = neighbours->begin(); it != neighbours->end(); it++) {
            auto this_node = *it;
            // Add any unvisited neighbours with matching chits.
            if(!visited[this_node.first][this_node.second] &&
               _chits[this_node.first][this_node.second] == who) {
                to_check.push(this_node);
            }
        }
        delete neighbours;
    }

    // Clean up.
    for(unsigned x = 0; x < _size; x++) {
        delete[] visited[x];
    }
    delete[] visited;
    
    return(win);
}

// Make a move at the given position.
void Board::move(unsigned x, unsigned y, Chits who)
{
    _chits[x][y] = who;
}
