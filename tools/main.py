import requests
import re
import json
from threading import Thread
import os


class ThreadingObject:
	onProgressCallback = None
	onSuccessCallback = None
	onErrorCallback = None	


class CMakeDocument(ThreadingObject):

	update_command_list_uri = 'http://www.cmake.org/cmake/help/v3.0/_sources/manual/cmake-commands.7.txt'
	update_command_doc_uri = 'http://www.cmake.org/cmake/help/v3.0/_sources/command/{command}.txt'

	command_doc = dict()

	update_variable_list_uri = 'http://www.cmake.org/cmake/help/v3.0/_sources/manual/cmake-variables.7.txt'
	update_variable_doc_uri = 'http://www.cmake.org/cmake/help/v3.0/_sources/variable/{variable}.txt'

	variable_doc = dict()

	def updateCommandDoc(self):
		try:
			new_command_doc = dict()
			
			response = requests.get(self.update_command_list_uri)

			command_pattern = re.compile(r'\/command\/(.+)')
			command_list = command_pattern.findall(response.content)
			if command_list:
				current_progress = 0
				total_progress = len(command_list)

				for command in command_list:
					if self.onProgressCallback:
						self.onProgressCallback(current_progress, total_progress)

					doc = requests.get(self.update_command_doc_uri.format(command = command)).content
					new_command_doc[command] = doc

					current_progress += 1
			else:
				raise Exception('Command list not found!')
			
			self.command_doc = new_command_doc
			if self.onSuccessCallback:
				self.onSuccessCallback()

		except Exception as ex:
			if self.onErrorCallback:
				self.onErrorCallback(ex)

		finally:
			self.onProgressCallback = None
			self.onErrorCallback = None
			self.onSuccessCallback = None

	def updateVariableDoc(self):
		try:
			new_variable_doc = dict()
			
			response = requests.get(self.update_variable_list_uri)

			variable_pattern = re.compile(r'\/variable\/(.+)')
			variable_list = variable_pattern.findall(response.content)
			if variable_list:
				current_progress = 0
				total_progress = len(variable_list)

				for variable in variable_list:
					if self.onProgressCallback:
						self.onProgressCallback(current_progress, total_progress)

					doc = requests.get(self.update_variable_doc_uri.format(variable = variable)).content
					new_variable_doc[variable] = doc

					current_progress += 1
			else:
				raise Exception('Variable list not found!')
			
			self.variable_doc = new_variable_doc
			if self.onSuccessCallback:
				self.onSuccessCallback()

		except Exception as ex:
			if self.onErrorCallback:
				self.onErrorCallback(ex)

		finally:
			self.onProgressCallback = None
			self.onErrorCallback = None
			self.onSuccessCallback = None

	def loadCommandDoc(self, fp):
		self.command_doc = json.load(fp)

	def saveCommandDoc(self, fp):
		json.dump(self.command_doc, fp, indent = 4)

	def loadVariableDoc(self, fp):
		self.variable_doc = json.load(fp)

	def saveVariableDoc(self, fp):
		json.dump(self.variable_doc, fp, indent = 4)

	def get(self, command):
		return self.command_doc.get(command)


def onProgress(current, total):
	print(current, total)

def onSuccess():
	print('success')

def onError(ex):
	print(ex)


class SublimeHelper:

	@staticmethod
	def createSnippet(fp, content, tab_trigger, scope):
		template = '''
<snippet>
	<content><![CDATA[
{content}
]]></content>
	<tabTrigger>{tab_trigger}</tabTrigger>
	<scope>{scope}</scope>
</snippet>'''

		fp.write(template.format(content = content, tab_trigger = tab_trigger, scope = scope))


def gen_sublime_completion(cmake_doc):
	cmake_sublime_completions = dict()
	cmake_sublime_completions['scope'] = 'source.cmake'
	cmake_sublime_completions['completions'] = []

	for command in cmake_doc.command_doc:
		cmake_sublime_completions.get('completions').append(command)

	for variable in cmake_doc.variable_doc:
		cmake_sublime_completions.get('completions').append(variable)

	with open('CMakeEditor.sublime-completions', 'wt') as fp:
		json.dump(obj = cmake_sublime_completions, fp = fp, indent = 4)


def save(cmake_doc):
	with open('command_doc.json', 'wt') as fp:
		cmake_doc.saveCommandDoc(fp)

	with open('variable_doc.json', 'wt') as fp:
		cmake_doc.saveVariableDoc(fp)


if __name__ == '__main__':
	cmake_doc = CMakeDocument()
	
	if os.path.exists('command_doc.json'):
		with open('command_doc.json', 'rt') as fp:
			cmake_doc.loadCommandDoc(fp)
	else:
		cmake_doc.onProgressCallback = onProgress
		cmake_doc.onSuccessCallback = onSuccess
		cmake_doc.onErrorCallback = onError

		Thread(target = cmake_doc.updateCommandDoc()).start()

	if os.path.exists('variable_doc.json'):
		with open('variable_doc.json', 'rt') as fp:
			cmake_doc.loadVariableDoc(fp)
	else:
		cmake_doc.onProgressCallback = onProgress
		cmake_doc.onSuccessCallback = onSuccess
		cmake_doc.onErrorCallback = onError

		Thread(target = cmake_doc.updateVariableDoc()).start()

	# save(cmake_doc)
	gen_sublime_completion(cmake_doc)