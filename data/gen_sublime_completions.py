import re
import os
import json


def main():
	doc_file = '2.8.12.2'
	if os.path.exists(doc_file):
		completion_list = []

		with open('2.8.12.2', 'rt') as fp:
			lines = fp.readlines()
			symbol_pattern = re.compile(r'^  \S+')
			
			for line in lines:
				match = symbol_pattern.match(line)
				if match:
					symbol = match.string.strip()
					# completion_list.append({'trigger': symbol, 'content': symbol})
					completion_list.append(symbol)

		sublime_completions = dict()
		sublime_completions['scope'] = 'source.cmakeeditor'
		sublime_completions['completions'] = completion_list

		with open('../CMakeEditor.sublime-completions', 'wt') as fp:
			json.dump(obj = sublime_completions, fp = fp, indent = 4)

	else:
		print('{file} not found.'.format(file = doc_file))


if __name__ == '__main__':
	main()
