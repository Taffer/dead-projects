/** Tests for hex2base64.
 *
 * This isn't using any unit test framework yet, just `assert()`.
 */

#include "hex2base64.h"

#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "greatest.h"

/** Test the `is_hex()` function.
 */
TEST test_is_hex(void)
{
    // Positive tests.
    ASSERT_EQm("Hex string isn't hex.", true, is_hex("1234567890abcdefABCDEF"));

    // Negative tests.
    ASSERT_EQm("Mixed string is hex.", false, is_hex("12345nope"));
    ASSERT_EQm("Empty string is hex.", false, is_hex(""));
    ASSERT_EQm("NULL string is hex.", false, is_hex(NULL));

    PASS();
}

/** Test the `char2hex()` function.
 */
TEST test_char2hex(void)
{
    // Positive tests.
    ASSERT_EQm("0 wasn't 0", 0x00, char2hex('0'));
    ASSERT_EQm("5 wasn't 5", 0x05, char2hex('5'));
    ASSERT_EQm("9 wasn't 9", 0x09, char2hex('9'));
    ASSERT_EQm("a wasn't 10", 0x0a, char2hex('a'));
    ASSERT_EQm("f wasn't 15", 0x0f, char2hex('f'));
    ASSERT_EQm("A wasn't 10", 0x0a, char2hex('A'));
    ASSERT_EQm("F wasn't 15", 0x0f, char2hex('F'));

    // Negative tests.
    ASSERT_EQm("z wasn't 0", 0, char2hex('z'));
    ASSERT_EQm(": wasn't 0", 0, char2hex(':'));

    PASS();
}

/** Test the `hex2bytes()` function.
 */
TEST test_hex2bytes(void)
{
    // Positive tests.
    {
        char hex[] = "deadbeef";
        unsigned char expected[] = {0xde, 0xad, 0xbe, 0xef};

        unsigned char *buffer = (unsigned char*)malloc(sizeof (hex) / 2);

        ASSERT_EQm("hex2bytes() failed.", CALL_OK, hex2bytes(hex, sizeof (hex) / 2, buffer));
        ASSERT_EQm("Output doesn't match expected values.", 0,
                   memcmp(expected, buffer, sizeof(hex) / 2));

        free(buffer);
        buffer = NULL;
    }

    {
        char hex[] = "1234567890abcdefABCDEF";
        unsigned char expected[] = {0x12, 0x34, 0x56, 0x78, 0x90, 0xab, 0xcd,
                                    0xef, 0xab, 0xcd, 0xef};

        unsigned char *buffer = (unsigned char*)malloc(sizeof (hex) / 2);

        ASSERT_EQm("hex2bytes() failed.", CALL_OK,
                   hex2bytes(hex, sizeof(hex) / 2, buffer));
        ASSERT_EQm("Output doesn't match expected values.", 0,
                   memcmp(expected, buffer, sizeof(hex) / 2));

        free(buffer);
        buffer = NULL;
    }

    // Negative tests.
    ASSERT_EQm("NULLs din't return NULL",
               CALL_BUFFER_NULL, hex2bytes(NULL, 0, NULL));
    ASSERT_EQm("Buffer wrote into NULL",
               CALL_BUFFER_NULL, hex2bytes("ffff", 0, NULL));
    {
        unsigned char *buffer = (unsigned char*)malloc(1024);
        ASSERT_EQm("Input buffer overflow worked.",
                   CALL_BAD_INPUT, hex2bytes("f", 1024, buffer));
        free(buffer);
        buffer = NULL;
    }
    {
        unsigned char *buffer = (unsigned char*)malloc(1);
        ASSERT_EQm("Output buffer overflow.",
                   CALL_BUFFER_OVERRUN, hex2bytes("deadbeef", 1, buffer));
        free(buffer);
        buffer = NULL;
    }

    PASS();
}

// Test bytes2hex().
TEST test_bytes2hex(void)
{
    // Positive tests.
    {
        uint8_t buffer[] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                            0x08, 0x09};
        char *str = NULL;
        retval_t retval = CALL_OK;

        retval = bytes2hex(buffer, sizeof(buffer), &str);
        ASSERT_EQm("Fail converting bytes to hex.", CALL_OK, retval);
        ASSERT_STR_EQm("Bytes didn't convert properly.",
                       "00010203040506070809", str);

        free(str);
        str = NULL;
    }
    {
        uint8_t buffer[] = {0xde, 0xad, 0xbe, 0xef};
        char *str = NULL;
        retval_t retval = CALL_OK;

        retval = bytes2hex(buffer, sizeof(buffer), &str);
        ASSERT_EQm("Fail converting bytes to hex.", CALL_OK, retval);
        ASSERT_STR_EQm("Bytes didn't convert properly.",
                       "deadbeef", str);

        free(str);
        str = NULL;
    }

    // Negative tests.
    ASSERT_EQm("NULL buffer converted to NULL output.",
               CALL_BUFFER_NULL, bytes2hex(NULL, 0, NULL));
    {
        uint8_t buffer[] = {0xde, 0xad, 0xbe, 0xef};
        ASSERT_EQm("Buffer converted to NULL output.",
                   CALL_BUFFER_NULL, bytes2hex(buffer, sizeof(buffer), NULL));
    }

    PASS();
}

// Test the `bytes2base64()` function.
TEST test_bytes2base64(void)
{
    // Negative tests.
    {
        retval_t retval = bytes2base64(0, NULL, 0, NULL);
        ASSERT_EQm("Encoded NULL into NULL.", CALL_BUFFER_NULL, retval);
    }
    {
        uint8_t bytes[] = "a string";
        retval_t retval = bytes2base64(sizeof(bytes), bytes, 0, NULL);
        ASSERT_EQm("Encoded a string into NULL.", CALL_BUFFER_NULL, retval);
    }
    {
        uint8_t bytes[] = "a string";
        char output[1];
        retval_t retval = bytes2base64(sizeof(bytes), bytes, sizeof(output), output);
        ASSERT_EQm("Encoded a string into one byte.", CALL_BUFFER_OVERRUN, retval);
    }
    {
        uint8_t bytes[] = "a string";
        char output[1];
        retval_t retval = bytes2base64(0, bytes, sizeof(output), output);
        ASSERT_EQm("Encoded 0 bytes.", CALL_BAD_INPUT, retval);
    }

    // Positive tests.
    {
        uint8_t bytes[] = {0x00};  // 1 byte = 4 output characters
        char *output = (char *)malloc(5);    // 4 chars + NUL
        retval_t retval = bytes2base64(sizeof(bytes), bytes, 5, output);

        ASSERT_EQm("Encoding 1 byte failed.", CALL_OK, retval);
        ASSERT_EQm("Output wrong size for 1 byte.", 4, strlen(output));
        ASSERT_STR_EQm("One NUL byte encoded wrong.", "AA==", output);

        free(output);
        output = NULL;
    }
    {
        uint8_t bytes[] = {0x00, 0x00};  // 2 bytes = 4 output characters
        char *output = (char *)malloc(5);    // 4 chars + NUL
        retval_t retval = bytes2base64(sizeof(bytes), bytes, 5, output);

        ASSERT_EQm("Encoding 2 bytes failed.", CALL_OK, retval);
        ASSERT_EQm("Output wrong size for 2 bytes.", 4, strlen(output));
        ASSERT_STR_EQm("Two NUL bytes encoded wrong.", "AAA=", output);

        free(output);
        output = NULL;
    }
    {
        uint8_t bytes[] = {0x00, 0x00, 0x00};  // 3 bytes = 4 output characters
        char *output = (char *)malloc(5);    // 4 chars + NUL
        retval_t retval = bytes2base64(3, bytes, 5, output);

        ASSERT_EQm("Encoding 3 bytes failed.", CALL_OK, retval);
        ASSERT_EQm("Output wrong size for 3 bytes.", 4, strlen(output));
        ASSERT_STR_EQm("Three NUL bytes encoded wrong.", "AAAA", output);

        free(output);
        output = NULL;
    }
    {
        uint8_t bytes[] = "Hello, world!";
        size_t padding = sizeof(bytes) % 3 == 0 ? 0 : 3 - sizeof(bytes) % 3;
        size_t target_length = (sizeof(bytes) / 3 + (padding > 0 ? 1 : 0)) * 4;
        char *output = (char *)malloc(target_length + 1);    // 4 chars + NUL
        retval_t retval = bytes2base64(sizeof(bytes), bytes, target_length + 1, output);

        ASSERT_EQm("Encoding Hello World failed.", CALL_OK, retval);
        ASSERT_EQm("Output wrong size for Hello World.", strlen(output), target_length);
        ASSERT_STR_EQm("Hello World encoded wrong.", "SGVsbG8sIHdvcmxkIQA=", output);

        free(output);
        output = NULL;
    }
    {
        uint8_t bytes[] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                           0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f};
        size_t padding = sizeof(bytes) % 3 == 0 ? 0 : 3 - sizeof(bytes) % 3;
        size_t target_length = (sizeof(bytes) / 3 + (padding > 0 ? 1 : 0)) * 4;
        char *output = (char *)malloc(target_length + 1);    // 4 chars + NUL
        retval_t retval = bytes2base64(sizeof(bytes), bytes, target_length + 1, output);

        ASSERT_EQm("Encoding 0x00 - 0x0f failed.", CALL_OK, retval);
        ASSERT_EQm("Output wrong size for 0x00 - 0x0f.", strlen(output), target_length);
        ASSERT_STR_EQm("0x00 - 0x0f encoded wrong.", "AAECAwQFBgcICQoLDA0ODw==", output);

        free(output);
        output = NULL;
    }

    PASS();
}

// Test the hex2base64() function.
TEST test_hex2base64(void)
{
    // Negative tests.
    retval_t retval = hex2base64(NULL, NULL);
    ASSERT_EQm("Encoding NULL into NULL.", CALL_BUFFER_NULL, retval);

    {
        char *hex = "DEADBEEF";
        retval = hex2base64(hex, NULL);
        ASSERT_EQm("Encoding into NULL.", CALL_BUFFER_NULL, retval);
    }

    // Positive tests.
    {
        char *hex = "DEADBEEF";
        char *expected = "3q2+7w==";
        char *output = NULL;
        retval = hex2base64(hex, &output);
        ASSERT_EQm("Encoding failed.", CALL_OK, retval);
        ASSERTm("Encoded to NULL.", output != NULL);
        ASSERT_STR_EQm("String encoded wrong.", expected, output);
        free(output);
        output = NULL;
    }

    PASS();
}

// Test the hex string we were sent here to check.
TEST set1_challenge1(void)
{
    char *hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d";
    char *expected = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t";
    char *output = NULL;
    retval_t retval = CALL_OK;

    retval = hex2base64(hex, &output);
    ASSERT_EQm("Conversion call failed.", CALL_OK, retval);
    ASSERT_STR_EQm("Failure!", expected, output);

    free(output);
    output = NULL;

    PASS();
}

SUITE(hex2base64_tests)
{
    RUN_TEST(test_is_hex);
    RUN_TEST(test_char2hex);
    RUN_TEST(test_hex2bytes);
    RUN_TEST(test_bytes2hex);
    RUN_TEST(test_bytes2base64);
    RUN_TEST(test_hex2base64);
}

SUITE(cryptopals_set1_challenge1)
{
    RUN_TEST(set1_challenge1);
}
