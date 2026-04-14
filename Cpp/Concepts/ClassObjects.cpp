#include <iostream>

class Book
{
private:
    std::string editorial;

public:
    std::string title;
    std::string author;
    int pages;
    // Constructor methods, equivalente al init
    Book(
        std::string name = "Default Instance",
        std::string title = "default tile",
        std::string author = "Anonimous",
        int pages = 500)
        : title(title),
          author(author),
          pages(pages)
    {
        std::cout << "Instance: " << this->title << " : " << name << std::endl;
    }

    // Setter
    void setEditorial(std::string editorial)
    {
    }

    std::string getEditorial()
    {
        return editorial;
    }
};

int main()
{
    Book book1("Book1");

    return 0;
}