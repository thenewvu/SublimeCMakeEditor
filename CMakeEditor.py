import sublime
import sublime_plugin
import json
import os
import re


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

	@staticmethod
	def loadResource(package_name, file_path):
		if hasattr(sublime, 'load_resource'):
			file_path = os.path.join('Packages', package_name, file_path)
			# for Windows we have to replace slashes
			file_path = file_path.replace('\\', '/')
			return sublime.load_resource(file_path)
		else:
			path = os.path.join(SublimeHelper.getPackagePath(package_name), file_path)
			with open(path, 'rt') as fp:
				return fp.read()


class CMakeEditorPlugin:

	name = 'CMakeEditor'

	symbol_index = None

	def __init__(self):

		self.doc_file = 'data/2.8.12.2'
		self.symbol_index_file = 'data/2.8.12.2.index'

		try:
			symbol_index_file_data = SublimeHelper.loadResource(self.name, self.symbol_index_file)
			self.symbol_index = json.loads(symbol_index_file_data)
		except Exception as ex:
			print(ex)
			SublimeHelper.printError('Load resource error on {file}. See log for detail.'.format(file = self.symbol_index_file))

	def getDoc(self, symbol):
		try:
			line_num = self.symbol_index.get(symbol)
			if line_num:
				doc_file_data = SublimeHelper.loadResource(self.name, self.doc_file)

				lines = doc_file_data.splitlines()
				line_count = len(lines)
				
				doc = ''
				symbol_pattern = re.compile(r'^  \S+')
				
				line_num += 1
				while line_num < line_count:
					line = lines[line_num]

					match = symbol_pattern.match(line)
					if not match:
						line = line.replace('       ', '')
						doc += '{line}\n'.format(line = line)
					else:
						break

					line_num += 1

				return doc
		except Exception as ex:
			print(ex)
			SublimeHelper.printError('Get document error. See log for detail.')


class CMakeEditorSearchDocCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		
		cmake_editor = CMakeEditorPlugin()

		symbol = SublimeHelper.getTextUnderCaret(self.view)
		doc = cmake_editor.getDoc(symbol)

		if doc:
			output_panel = sublime.active_window().get_output_panel(cmake_editor.name)
			output_panel.run_command('c_make_editor_show_doc', {'text': doc, 'ouput_panel_name': cmake_editor.name})
		else:
			SublimeHelper.printStatus('Not found document for \"{symbol}\" !'.format(symbol = symbol))


class CMakeEditorShowDocCommand(sublime_plugin.TextCommand):

	def run(self, edit, text, ouput_panel_name):
		self.view.insert(edit, 0, text)

		self.view.settings().set('draw_centered', True)

		sublime.active_window().run_command("show_panel", {"panel": "output.{panel_name}".format(panel_name = ouput_panel_name)})
