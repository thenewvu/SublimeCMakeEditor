## Features

* Quick Reference
* Auto-Completion
* Syntax Highlight

![CMake Quick Reference](http://i.imgur.com/cpzbLwJ.png "CMake Quick Reference")

![CMake Auto-Completion](http://i.imgur.com/j9QL3Cg.png "CMake Auto-Completion")

## How to use ?

**Requirements**:

Change the file syntax to `CMakeEdit` by `View > Syntax > CMakeEditor`.

**To reference a symbol**:

Put the cursor on the symbol, press F1.

**To change hotkey**:

Goto `Preferences > Package Settings > CMakeEditor > Key Bindings - User`, paste then edit this:

```
[
	{
		"keys": ["f1"],
		"command": "c_make_editor_search_doc",
		"context": [
			{ "key": "selector", "operator": "equal", "operand": "source.cmakeeditor" }
		]
	}
]
```

## Thank to

@Piepenguin1995  
@mtuchowski  
@alexey-broadcast  
