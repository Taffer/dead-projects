/** @file hex2base64 implementation.
 *
 * See hex2base64.h for details.
 */

#include "hex2base64.h"

#include <ctype.h>
#include <limits.h>
#include <stdbool.h>
#include <string.h>

// Are the characters in hexstr all hex digits?
bool is_hex(const char *hexstr)
{
	bool retval = true;
	size_t idx = 0;
	size_t hexstr_length = 0;

	// Sanity
	if(NULL == hexstr) {
		return false;
	}

	hexstr_length = strnlen(hexstr, UINT_MAX);
	if(hexstr_length < 1) {
		// Empty string is not a hex value.
		retval = false;
	}

	idx = 0;
	while(idx < hexstr_length && true == retval) {
		if(!isxdigit((int)hexstr[idx])) {
			retval = false;
		}
		idx++;
	}

	return retval;
}

// Convert one hex digit to its value.
uint8_t char2hex(const char a_char)
{
    uint8_t retval = 0;

    if(a_char >= 48 && a_char <= 57) {
        retval = (uint8_t)a_char - 48;  // '0' - '9'
    }else if (a_char >= 65 && a_char <= 70) {
        retval = (uint8_t)a_char - 55;  // 'A' - 'F'
    }else if (a_char >= 97 && a_char <= 102) {
        retval = (uint8_t)a_char - 87;  // 'a' - 'f'
    }

    return retval;
}

// Convert a string of hex digits into the bytes they represent.
retval_t hex2bytes(const char *hexstr, size_t byte_length, uint8_t *bytes)
{
    size_t hexstr_length = 0;
    size_t x = 0;

    // Sanity checking.
    if(NULL == hexstr) {
        return CALL_BUFFER_NULL;
    }

    if(NULL == bytes) {
        return CALL_BUFFER_NULL;
    }

    // Don't overflow me, bro.
    hexstr_length = strnlen(hexstr, UINT_MAX);
    if(hexstr_length % 2 == (size_t)1) {
        return CALL_BAD_INPUT;
    }
    if((hexstr_length / 2) > byte_length) {
        return CALL_BUFFER_OVERRUN;
    }

    // Now the easy part.
    x = 0;
    while(x < hexstr_length) {
        uint8_t byte = (uint8_t)(char2hex(hexstr[x]) << 4) + char2hex(hexstr[x + 1]);
		bytes[x / 2] = byte;
        x += 2;
    }

    return CALL_OK;
}

// Hexadecimal characters.
static const char HEX_CHARS[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8',
                                 '9', 'a', 'b', 'c', 'd', 'e', 'f'};

// Convert a buffer of bytes into a string of hex digits.
retval_t bytes2hex(const uint8_t *bytes, const size_t bytes_length,
                   char **hexstr)
{
    size_t x = 0;
    size_t hexstr_length = 0;
    char *tmpstr = NULL;

    // Sanity checking.
    if(NULL == bytes) {
        return CALL_BUFFER_NULL;
    }

    if(NULL == hexstr) {
        return CALL_BUFFER_NULL;
    }

    // Just say no to overflow.
    hexstr_length = bytes_length * 2 + 1;  // Don't forget NUL.
    tmpstr = (char *)malloc(hexstr_length);
    if(NULL == tmpstr) {
        return CALL_BUFFER_NULL;
    }
    *hexstr = tmpstr;

    // Lazy implementation. :-)
    x = 0;
    while(x < bytes_length) {
        uint8_t top_half = (bytes[x] & UINT8_C(0xf0)) >> 4;
        uint8_t bottom_half = bytes[x] & UINT8_C(0x0f);
        *tmpstr++ = HEX_CHARS[top_half];
        *tmpstr++ = HEX_CHARS[bottom_half];
        x++;
    }
    *tmpstr = '\0';

    return CALL_OK;
}

// MIME base64 encoding
static const char BASE64_CHARS[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                    'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                                    'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                    'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
                                    'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                    'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                                    'w', 'x', 'y', 'z', '0', '1', '2', '3',
                                    '4', '5', '6', '7', '8', '9', '+', '/'};

static const char BASE64_PAD = '=';

// Convert a buffer of bytes into its base64 representation.
retval_t bytes2base64(const size_t bytes_length, const uint8_t *bytes,
                      size_t base64str_length, char *base64str)
{
    size_t target_length = 0;
    size_t padding = 0;
    size_t idx = 0;

    // Sanity!
    if(NULL == bytes) {
        return CALL_BUFFER_NULL;
    }

    if(NULL == base64str) {
        return CALL_BUFFER_NULL;
    }

    if(bytes_length < 1) {
        return CALL_BAD_INPUT;
    }

    padding = bytes_length % 3 == 0 ? 0 : 3 - bytes_length % 3;
    target_length = (bytes_length / 3 + (padding > 0 ? 1 : 0)) * 4;
    if(base64str_length < (target_length + 1)) {  // +1 for NUL
        return CALL_BUFFER_OVERRUN;
    }

    // Start fresh.
    memset(base64str, 0, base64str_length);

    while((idx + 3) <= bytes_length) {
        uint32_t bits = (uint32_t)bytes[idx] << 16     |  // byte 1 = bits 17 - 24
                        (uint32_t)bytes[idx + 1] << 8  |  // byte 2 = bits 9 - 16
                        (uint32_t)bytes[idx + 2];         // byte 3 = bits 1 - 8
        idx += 3;

        *base64str++ = BASE64_CHARS[(bits & 0xfc0000) >> 18];  // bits 19 - 24
        *base64str++ = BASE64_CHARS[(bits & 0x03f000) >> 12];  // bits 13 - 18
        *base64str++ = BASE64_CHARS[(bits & 0x000fc0) >> 6];   // bits 7 - 12
        *base64str++ = BASE64_CHARS[(bits & 0x00003f)];        // bits 1 - 6
    }

    if(padding > 0) {
        uint32_t bits = 0;
        if(2 == padding) {
            bits = (uint32_t)bytes[idx] << 16;     // byte 1 = bits 17 - 24
        } else {  // 1 == padding
            bits = (uint32_t)bytes[idx] << 16   |  // byte 1 = bits 17 - 24
                   (uint32_t)bytes[idx + 1] << 8;  // byte 2 = bits 8 - 15
        }

        *base64str++ = BASE64_CHARS[(bits & 0xfc0000) >> 18];     // bits 19 - 24
        *base64str++ = BASE64_CHARS[(bits & 0x03f000) >> 12];     // bits 13 - 18
        if(2 == padding) {
            *base64str++ = BASE64_PAD;                            // bits 7 - 12
        } else {
            *base64str++ = BASE64_CHARS[(bits & 0x000fc0) >> 6];  // bits 7 - 12
        }
        *base64str++ = BASE64_PAD;                                // bits 1 - 6
    }

    return CALL_OK;
}

// Convert a string of hex digits into its base64 representation.
retval_t hex2base64(const char *hexstr, char **base64str)
{
    retval_t retval = CALL_OK;
    size_t bytes_length = 0;
    size_t padding = 0;
    size_t base64_length = 0;
    uint8_t *bytes = NULL;

    // Sanity
    if(NULL == hexstr) {
        return CALL_BUFFER_NULL;
    }

    if(NULL == base64str) {
        return CALL_BUFFER_NULL;
    }

    // Convert hex to bytes.
    bytes_length = strnlen(hexstr, UINT_MAX) / 2;
    bytes = (uint8_t *)malloc(bytes_length);
    retval = hex2bytes(hexstr, bytes_length, bytes);
    if(CALL_OK != retval) {
        free(bytes);
        return CALL_BAD_INPUT;
    }

    // Convert bytes to base64.
    padding = bytes_length % 3 == 0 ? 0 : 3 - bytes_length % 3;
    base64_length = (bytes_length / 3 + (padding > 0 ? 1 : 0)) * 4;
    *base64str = (char *)malloc(base64_length + 1);
    retval = bytes2base64(bytes_length, bytes, base64_length + 1, *base64str);
    if(CALL_OK != retval) {
        free(*base64str);
        *base64str = NULL;
    }

    free(bytes);

    return CALL_OK;
}
