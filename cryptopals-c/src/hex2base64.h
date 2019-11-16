/** @file Utilities for converting strings of hexadecimal into base64.
 *
 * Implements the first
 * [Cryptopals challenge](http://cryptopals.com/sets/1/challenges/1/),
 * in addition to several helper functions.
 *
 * Given a string of hexadecimal characters:
 *
 * * convert them to a binary string of bytes
 * * convert those into a base64 string
 *
 * Swank pug logo from [Turbomilk](http://turbomilk.com/)'s
 * [Zoom-Eyed Creatures](https://www.iconfinder.com/iconsets/zoomeyed).
 */

#ifndef CRYPTOPALS_HEX2BASE64_H
#define CRYPTOPALS_HEX2BASE64_H

#include <stdbool.h>  // C99 or GTFO
#include <stdint.h>
#include <stdlib.h>

#include "retval.h"

#ifdef __cplusplus
extern "C" {
#endif

/** Is the given string made up entirely of hexadecimal characters?
 *
 * Note that this will return false for nonsensical strings too, such as
 * `NULL` or an empty string.
 *
 * @param[in] hexstr Pointer to a C string.
 *
 * @return true or false
 */
bool is_hex(const char *hexstr);

/** Convert a hexadecimal character into its value.
 *
 * @bug Returns 0 for non-hex characters.
 *
 * @param[in] a_char A character.
 *
 * @return The character's value as a hex digit.
 */
uint8_t char2hex(const char a_char);

/** Given a string of hex, convert it into bytes.
 *
 * Note that bytes will NOT be `NUL` terminated as it's not a string. Don't
 * treat it like one.
 *
 * @param[in] hexstr A string of hex digits.
 * @param[in] byte_length Length of the output buffer.
 * @param[out] bytes A buffer to receive the bytes; must be the right size.
 *
 * @return Returns an error code or CALL_OK.
 */
retval_t hex2bytes(const char *hexstr, size_t byte_length, uint8_t *bytes);

/** Given a buffer of bytes, convert it into a string of hex characters.
 *
 * hexstr will be NULL if the encoding fails. Don't free() it if it's NULL.
 *
 * @param[in] bytes A buffer of bytes.
 * @param[in] bytes_length Length of the bytes buffer.
 * @param[out] hexstr A pointer to a buffer; you must free it when done.
 *
 * @return Returns an error code or CALL_OK.
 */
retval_t bytes2hex(const uint8_t *bytes, const size_t bytes_length,
                   char **hexstr);

/** Convert a buffer of bytes into base64.
 *
 * @param[in] bytes_length Length of the input buffer.
 * @param[in] bytes The input buffer.
 * @param[in] base64str_length Length of the output buffer.
 * @param[out] base64str The output buffer.
 *
 * @return Returns an error code or CALL_OK.
 */
retval_t bytes2base64(const size_t bytes_length, const uint8_t *bytes,
                      size_t base64str_length, char *base64str);


/** Convert a hex string to the base64 representation of its bytes.
 *
 * Allocates a suitably-sized buffer for the base64 string and returns it
 * in base64str. Caller must free() base64str, which is NUL-terminated.
 *
 * base64str will be NULL if the encoding fails. Don't free() it if it's NULL.
 *
 * @param[in] hexstr A string of hex digits.
 * @param[out] base64str A pointer to a buffer; you must free it when done.
 *
 * @return Returns an error code or CALL_OK.
 */
retval_t hex2base64(const char *hexstr, char **base64str);

#ifdef __cplusplus
}
#endif

#endif /* CRYPTOPALS_HEX2BASE64_H */
