import sublime
import sublime_plugin
import json
import os


class SublimeHelper:

	@staticmethod
	def getTextUnderCaret(view):
		'''
			return selecting text or text under the caret
		'''

		text = None

		if view.sel:
			region = view.sel()[0]

			if region.begin() == region.end():
				region = view.word(region)
			
			text = view.substr(region)

		return text

	@staticmethod
	def printStatus(message):
		sublime.status_message(message)

	@staticmethod
	def printError(message):
		sublime.error_message(message)

	@staticmethod
	def printLog(message):
		print(message)

	@staticmethod
	def getPackagePath(package):
		return os.path.join(sublime.packages_path(), package)


class CMakeDoc:

	doc = None

	def load(self, fp):
		self.doc = json.load(fp)

	def get(self, symbol):
		if self.doc:
			return self.doc.get(symbol)
		else:
			return None


class CMakeEditorPlugin:

	name = 'CMakeEditor'
	path = SublimeHelper.getPackagePath(name)

	doc = CMakeDoc()
	doc_file = os.path.join(path, 'doc.json')

	def __init__(self):
		if os.path.exists(self.doc_file):
			with open(self.doc_file, 'rt') as fp:
				self.doc.load(fp)
		else:
			SublimeHelper.printError('Not found {file}. Please reinstall CMakeEditor plugin.'.format(file = self.doc_file))

	def getDoc(self, symbol):
		return self.doc.get(symbol)


class CMakeEditorSearchDocCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		
		cmake_editor_plugin = CMakeEditorPlugin()

		symbol = SublimeHelper.getTextUnderCaret(self.view)
		doc = cmake_editor_plugin.getDoc(symbol)

		if doc:
			output_panel = sublime.active_window().get_output_panel(cmake_editor_plugin.name)
			output_panel.run_command('c_make_editor_show_doc', {'text': doc, 'ouput_panel_name': cmake_editor_plugin.name})
		else:
			SublimeHelper.printStatus('Not found document for \"{symbol}\" !'.format(symbol = symbol))


class CMakeEditorShowDocCommand(sublime_plugin.TextCommand):
	def run(self, edit, text, ouput_panel_name):
		self.view.insert(edit, 0, text)
		sublime.active_window().run_command("show_panel", {"panel": "output.{panel_name}".format(panel_name = ouput_panel_name)})
