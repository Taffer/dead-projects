/** @file Return values.
 */

#ifndef CRYPTOPALS_RETVAL_H
#define CRYPTOPALS_RETVAL_H

#ifdef __cplusplus
extern "C" {
#endif

/** Function return values.
 */
typedef uint_fast32_t retval_t;

#define CALL_OK             0  ///< Success!

#define CALL_BUFFER_OVERRUN 1  ///< Output buffer isn't big enough.
#define CALL_BUFFER_NULL    2  ///< Buffer is NULL.

#define CALL_BAD_INPUT      3  ///< Input values are bad.

#ifdef __cplusplus
}
#endif

#endif
