#include <iostream>
#include <string>

int main()
{
    int age = 19;
    int *pAge = &age;
    double esto = 2.7;
    double *pEsto = &esto;
    std::string fuck = "0";
    std::string *pFuck = &fuck;

    // cada una de estas variables esta en un
    // contenedor en la memoria ram y cada una tiene una direccion en la memoria
    // Imprimir la direccion de memoria fisica, las addresses son los pointers
    std::cout << age << " : " << pAge << " : " << *pAge << " : " << *&age; // ej. 0x4fdfff8f8
    return 0;
}