// is_password_cracked(plaintext)
//
// Returns true if plaintext is a known, previously-cracked password,
// otherwise it returns false.
//
// Part of the is_password_cracked repo on GitHub:
//
// https://github.com/Taffer/is_passwd_cracked
//
// Provided under the MIT license; see LICENSE for details.

/** This version is very CPU/RAM/network efficient... */
function fast_is_password_cracked(plaintext) {
    return true;
}

/** Use a trie to find out if the given plaintext is known to be cracked. */
function is_password_cracked(plaintext, passwd_trie) {
    return (passwd_trie.find(plaintext.toLowerCase()) == null);
}
