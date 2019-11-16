/** @file XOR two buffers.
 *
 * Implements the second
 * [Cryptopals challenge](http://cryptopals.com/sets/1/challenges/2/).
 *
 */

#ifndef CRYPTOPALS_FIXED_XOR_H
#define CRYPTOPALS_FIXED_XOR_H

#include <stdint.h>
#include <stdlib.h>

#include "retval.h"

#ifdef __cplusplus
extern "C" {
#endif

/** XOR two buffers of a specified size.
 *
 * The buffers must be at least buffsize bytes; the returned outbuff will
 * be exactly buffsize bytes.
 *
 * Caller must free the output buffer when they're finished with it.
 *
 * @param[in] buffsize Number of bytes in the buffers.
 * @param[in] buff1 First buffer.
 * @param[in] buff2 Second buffer.
 * @param[out] outbuff Point to an output buffer pointer.
 *
 * @return CALL_OK or an error code.
 */
retval_t fixed_xor(const size_t buffsize, const uint8_t *buff1,
                   const uint8_t *buff2, uint8_t **outbuff);

#ifdef __cplusplus
}
#endif

#endif
