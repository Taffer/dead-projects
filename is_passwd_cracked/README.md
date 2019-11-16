# is_passwd_cracked

So, Dan Tentler (@Viss) had a [great idea](https://twitter.com/Viss/status/506974673012146176);
why not use the existing lists of stolen and cracked passwords to make
something to stop people from using those passwords again.

This is a cool problem because the dataset is simple, but pretty huge; I
downloaded around 68MB of passwords from [SkullSecurity](https://wiki.skullsecurity.org/Passwords)
to get started.

This repo has a collection of bits, MIT-licensed, so you can take advantage of
others' misfortunes by making it easy to stop users from re-using these
already-compromised passwords.

Things to do:

* Whip up a Python script to convert a directory full of password lists into a single deduped list.
* Decent server-side example of `is_passwd_cracked()` (probably Python with Flask at first).
* Figure out a clever way of making this not suck on the client in JavaScript.

The client-side version would do all the checking on the client, before
transmitting anything to the server. The server-side version has the potentially
bit disadvantage of sending the user's password to the server, where people can
do all kinds of stupid things.

**PROTIP**: Never, ever store user's passwords. Use a cryptographic hash
function (such as SHA1) *and* some salt and store the resulting salted hash
instead.

**PROTIP**: No, you don't need to be able to send a user their password. Ever.

Seriously, you don't. If you can recover someone's password, so can an
adversary.

Here's a fast but inaccurate Python version to tide you over:

```python
def is_passwd_cracked(plaintext_string):
    ''' Has this password been cracked already? (Fast but inaccurate.)

    :param plaintext_string: Plain text password to check.
    '''
    return True
```

## Credits

* JavaScript trie implementation by [Mike de Boer](https://github.com/mikedeboer/trie).
