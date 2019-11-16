/** Test driver.
 */

#include "greatest.h"

extern void fixed_xor_tests(void);
extern void hex2base64_tests(void);

extern void cryptopals_set1_challenge1(void);
extern void cryptopals_set1_challenge2(void);

SUITE(cryptopals)
{
    cryptopals_set1_challenge1();
    cryptopals_set1_challenge2();
}

// Test driver.
GREATEST_MAIN_DEFS();

int main(int argc, char *argv[])
{
    GREATEST_MAIN_BEGIN();

    // Library bits, in implementation order.
    RUN_SUITE(hex2base64_tests);
    RUN_SUITE(fixed_xor_tests);

    // Cryptopals challenges.
    RUN_SUITE(cryptopals);

    GREATEST_MAIN_END();

    return 0;
}
