# Apache Configuration

To use Pug with Apache, you need to install and/or enable `mod_wsgi`.

The suggested site configuration for Pug is:

```xml
WSGIDaemonProcess pug user=pug-user group=pug-group processes=4 threads=5
WSGIScriptAlias / /path/to/pug/pug_wsgi.py

<Directory /path/to/pug>
	WSGIPassAuthorization On
	WSGIScriptReloading Off
	WSGIRestrictEmbedded On
	WSGIProcessGroup pug
	WSGIApplicationGroup %{GLOBAL}

	Order deny,allow
	Allow from all
</Directory>
```

* `processes=4` assumes a web server with two cores, and that 2 &times; cores is a good default.
* Change `pug-user` and `pug-group` to the user and group you want to run the Pug application as.
* Change `/path/to/pug` to be the path to your Pug installation. The `pug-user` will need read access to this directory tree.

If you need to tweak the `mod_wsgi` configuration, you can find its directives here: http://code.google.com/p/modwsgi/wiki/ConfigurationDirectives
