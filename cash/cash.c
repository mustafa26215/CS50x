#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int cents;

    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    int quarters = 0;
    while (cents >= 25)
    {
        quarters++;
        cents = cents - 25;
    }

    int dimes = 0;
    while (cents >= 10)
    {
        dimes++;
        cents = cents - 10;
    }

    int nickels = 0;
    while (cents >= 5)
    {
        nickels++;
        cents = cents - 5;
    }

    int pennies = 0;
    while (cents >= 1)
    {
        pennies++;
        cents = cents - 1;
    }

    int coins = quarters + dimes + nickels + pennies;

    printf("%i\n", coins);
}
