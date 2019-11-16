/** @file fixed_xor implementation.
 *
 * See fixed_xor.h for details.
 */

#include "fixed_xor.h"

retval_t fixed_xor(const size_t buffsize, const uint8_t *buff1,
                   const uint8_t *buff2, uint8_t **outbuff)
{
    // Sanity
    if(buffsize < 1) {
        return CALL_BAD_INPUT;
    }

    if(buff1 == NULL || buff2 == NULL || outbuff == NULL) {
        return CALL_BUFFER_NULL;
    }

    // Allocate and XOR
    uint8_t *tmpbuff = (uint8_t *)malloc(buffsize);
    if(tmpbuff == NULL) {
        return CALL_BUFFER_NULL;
    }

    for(size_t x = 0; x < buffsize; x++) {
        tmpbuff[x] = buff1[x] ^ buff2[x];
    }

    *outbuff = tmpbuff;

    return CALL_OK;
}
