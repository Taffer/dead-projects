# Pug

A Scrum project manager.

At work I've used several Agile project managers, and none of them seemed to
handle Scrum teams very well. This is my attempt to make something better.

## Requirements

This is a Python 2.7 web service. You'll need:

* Apache with `mod_wsgi` or another web server that supports WSGI apps.
* Python 2.7.*x*, where *x* is the latest release. Please try to keep up.
* Additional Python modules:
  * bcrypt - https://pypi.python.org/pypi/bcrypt/
  * Flask - http://flask.pocoo.org/
  You can install these via `pip` or your favourite package manager:
  ```bash
  pip install bcrypt flask
  ```
+
## Configuration

To customize your Pug installation:

1. Add any general configuration entries (from the root `config.py`) you need to customize to a root `local_config.py`; entries in `local_config.py` override the entries in `config.py`, so you only need to make `local_config.py` entries for things that need to be changed.

## License

Pug is released under an MIT license; see the LICENSE file for details.

Pug uses additional resources provided under different licenses; see the
Credits, below, for details.

## Credits

The project name is inspired by my dog Bella. You can probably find pictures
of her on 500px: https://500px.com/punksdad

Pug is designed and developed by Chris Herborth; the code is published on
GitHub: https://github.com/Taffer/Pug

### Open Source

These open source projects are free to use, even for commercial purposes:

* Bootstrap - http://getbootstrap.com/
* is_passwd_cracked - https://github.com/Taffer/is_passwd_cracked
* jQuery - http://jquery.com/

These open source projects are free but have custom licenses you may want to
investigate:

* CommonMark-py - https://github.com/rolandshoemaker/CommonMark-py
* Emoji - https://github.com/carpedm20/emoji

Note that I changed emoji.emojize() slightly so it wouldn't eat unknown Emoji
shortcuts. For example, `:bella_is_my_pug:` will be passed through untouched.

### Resources

If you're installing Pug at work, you'll need to replace these resources, which
are free to use, but *not* for commercial purposes:

* Pug icon - http://turbomilk.com/ (part of http://findicons.com/pack/624/zoom_eyed_creatures)
