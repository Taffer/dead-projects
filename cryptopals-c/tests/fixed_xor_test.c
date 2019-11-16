/** Tests for fixed_xor.
 *
 * This isn't using any unit test framework yet, just `assert()`.
 */

#include "fixed_xor.h"

#include <stdlib.h>
#include <string.h>

#include "greatest.h"
#include "hex2base64.h"

TEST test_fixed_xor(void)
{
    uint8_t buff[] = {0x13, 0x37};
    uint8_t expected[] = {0x00, 0x00};

    uint8_t *outbuff = NULL;

    // Positive tests.
    ASSERT_EQm("fixed_xor didn't work", CALL_OK, fixed_xor(sizeof(buff), buff, buff, &outbuff));
    ASSERT_EQm("Result didn't match expected", 0, memcmp(outbuff, expected, sizeof(buff)));

    // Negative tests.
    ASSERT_EQm("Bad length fail", CALL_BAD_INPUT, fixed_xor(0, NULL, NULL, NULL));

    ASSERT_EQm("Valid buff1 fail", CALL_BUFFER_NULL, fixed_xor(sizeof(buff), buff, NULL, NULL));
    ASSERT_EQm("Valid buff2 fail", CALL_BUFFER_NULL, fixed_xor(sizeof(buff), buff, buff, NULL));

    PASS();
}

TEST set1_challenge2(void)
{
    char *buff1 = "1c0111001f010100061a024b53535009181c";
    char *buff2 = "686974207468652062756c6c277320657965";
    char *expected = "746865206b696420646f6e277420706c6179";

    uint8_t *buff1_bytes = (uint8_t *)malloc(strlen(buff1));
    uint8_t *buff2_bytes = (uint8_t *)malloc(strlen(buff2));
    uint8_t *expected_bytes = (uint8_t *)malloc(strlen(expected));

    size_t numbytes = strlen(expected) / 2;

    if(buff1_bytes == NULL || buff2_bytes == NULL || expected_bytes == NULL) {
        FAILm("Unable to allocate buffers.");
    }

    retval_t retval = hex2bytes(buff1, numbytes, buff1_bytes);
    if(retval != CALL_OK) {
        FAILm("Unable to convert buff1 to bytes.");
    }
    retval = hex2bytes(buff2, numbytes, buff2_bytes);
    if(retval != CALL_OK) {
        FAILm("Unable to convert buff2 to bytes.");
    }
    retval = hex2bytes(expected, numbytes, expected_bytes);
    if(retval != CALL_OK) {
        FAILm("Unable to convert expected to bytes.");
    }

    uint8_t *result = NULL;
    retval = fixed_xor(numbytes, buff1_bytes, buff2_bytes, &result);
    if(retval != CALL_OK) {
        FAILm("fixed_xor() failed");
    }

    ASSERT_EQm("Result didn't match expected", 0, memcmp(result, expected_bytes, numbytes));

    free(result);
    free(expected_bytes);
    free(buff2_bytes);
    free(buff1_bytes);

    PASS();
}

SUITE(fixed_xor_tests)
{
    RUN_TEST(test_fixed_xor);
}

SUITE(cryptopals_set1_challenge2)
{
    RUN_TEST(set1_challenge2);
}
