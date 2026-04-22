#include <iostream>
#include <string>
#include <vector>

struct Position
{
    int x, y;
};

class Piece
{
public:
    Position pos;
    Piece(Position pos) : pos(pos) {};

    // el = 0 significa que obligatoriamente las hijas lo deben definir y aqui no importa
    virtual std::vector<Position> get_positions() = 0;

    virtual Position move_to(Position new_pos)
    {
        pos = new_pos;
    }

    virtual ~Piece() = default; // Destructor, default es para usar el destructor del compilador
};

class peon : public Piece
{
};

class caballo : public Piece
{
public:
    std::vector<Position> get_positions()
    {
        // la Esto debe recibir como entrada
        // std::vector<std::vector<int>> board(8, std::vector<int>(8));

        // Teorical positions
        for (int f = pos.x - 2; f <= pos.x - 1; f++)
        {
            int factor = 1;
            for (int c = pos.y - factor; c <= pos.y + factor; c += 2 * factor)
            {
                factor = 2;
            }
        }
    }
};

/*
Forma elegante
std::vector<std::vector<int>> get_submatrix(int map[8][8], int x, int y) {
    std::vector<std::vector<int>> sub;

    for (int i = x - 2; i <= x + 2; i++) {
        std::vector<int> row;
        for (int j = y - 2; j <= y + 2; j++) {
            if (i >= 0 && i < 8 && j >= 0 && j < 8)
                row.push_back(map[i][j]);
        }
        sub.push_back(row);
    }

    return sub;
}


*/