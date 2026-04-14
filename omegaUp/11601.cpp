#include <iostream>
#include <vector>

int main()
{
    int n, m, i, o;

    std::cin >> n >> m;

    // Validaciones basicas
    if (n > 0 && m > 0)
    {
        std::vector<int> p(n);
        std::vector<int> v(m + 1, 0);

        for (i = 0; i < n; i++)
        {
            std::cin >> o;
            p[i] = o;

            if (o > 0 && o <= m)
            {
                v[o] += 1;
            }
        }

        for (i = 1; i <= m; i++)
        {

            std::cout << i << ": " << v[i] << std::endl;
        }
    };

    return 0;
}