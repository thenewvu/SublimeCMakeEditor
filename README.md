Sublime CMake Editor
====================

A Sublime Text 2/3 plugin that provides CMake quick reference, auto-completion and syntax highlight features.

Features
--------

* CMake Quick Reference (ver 2.8.12.2)
* CMake Auto-Completion (ver 2.8.12.2)
* CMake Syntax Highlight

![CMake Quick Reference](http://i.imgur.com/cpzbLwJ.png "CMake Quick Reference")

![CMake Auto-Completion](http://i.imgur.com/j9QL3Cg.png "CMake Auto-Completion")

Usage
-----

**Requirement**

First, you need to set your document syntax to 'CMakeEditor' by choosing: View -> Syntax -> CMakeEditor

**Quick Reference**

Click on the symbol then press F1

Customize
---------

This is the default keymap:

	[
		{
			"keys": ["f1"],
			"command": "c_make_editor_search_doc",
			"context": [
				{ "key": "selector", "operator": "equal", "operand": "source.cmakeeditor" }
			]
		}
	]

To tweak it, copy the default -> choose Preferences -> Package Settings -> CMakeEditor -> Key Bindings - User -> paste the default and change 'keys' value as you want.

Changelog
---------

* 10/10/2014 - 1.0.0 beta - the first version

Get Involved ?
--------------

* Donate via [Gittip](https://www.gittip.com/thenewvu/)
* Contribute via [Github](https://github.com/thenewvu/SublimeCMakeEditor)