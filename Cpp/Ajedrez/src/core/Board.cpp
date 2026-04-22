#include <iostream>

class Board
{
public:
    int board[8][8];

    Board()
    {
        std::cout << board[2][2];
    };
};

int main()
{
    Board board;
}