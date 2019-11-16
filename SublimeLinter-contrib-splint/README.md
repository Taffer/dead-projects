# SublimeLinter-contrib-splint

**Abandoned!** I've abandoned this (not that there was much here in the first place) as I'm not going to use splint for the project I had in mind.

A plugin for [SublimeLinter](http://sublimelinter.readthedocs.org/) providing an
interface to [splint](http://splint.org/). It will be used with files that have
the "C" syntax.

Splint is a C linter that attempts to find security vulnerabilities in addition
to the usual coding and stylistic mistakes.

## Installation

### Linter Installation

Be sure that `splint` is installed on your system before attempting to use this
linter; generally something like:

    {platform package manager} install splint

* On Mac, use [Homebrew](http://brew.sh/): `brew install splint`
* On Cygwin, use the Cygwin `setup.exe` and search for `splint`.

Once `splint` is installed, you must ensure it is in your system `PATH` so that
SublimeLinter can find it. This may not be as straightforward as you think, so
please read about
[how linter executables are located](http://sublimelinter.readthedocs.org/en/latest/usage.html#how-linter-executables-are-located)
in the documentation.

SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter
3 is not installed, please follow the instructions
[here](http://www.sublimelinter.com/en/latest/installation.html).

### Plugin installation

Please use [Package Control](https://packagecontrol.io/installation) to install
the linter plugin. This will ensure that the plugin will be updated when new
versions are available. If you want to install from source so you can modify the
source code, you probably know what you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the
[Command Palette](http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html)
and type `install`. Among the commands you should see `Package Control: Install
Package`. If that command is not highlighted, use the keyboard or mouse to
select it. There will be a pause of a few seconds while Package Control fetches
the list of available plugins.

1. When the plugin list appears, type `splint`. Among the entries you should see
`SublimeLinter-contrib-splint`. If that entry is not highlighted, use the
keyboard or mouse to select it.

## Configuration

## Settings

## Examples
