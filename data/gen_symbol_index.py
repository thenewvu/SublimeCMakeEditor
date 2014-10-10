import re
import os
import json


def main():
	cmake_version = '2.8.12.2'

	doc_file = cmake_version
	if os.path.exists(doc_file):
		with open(doc_file, 'rt') as fp:
			lines = fp.readlines()
			line_num = 0
			symbol_pattern = re.compile(r'^  \S+')
			symbol_index = dict()

			for line in lines:
				match = symbol_pattern.match(line)
				if match:
					symbol_index[match.string.strip()] = line_num

				line_num += 1

			with open('{version}.index'.format(version = cmake_version), 'wt') as index_file:
				json.dump(obj = symbol_index, fp = index_file, indent = 4)

	else:
		print('{file} not found.'.format(file = doc_file))


if __name__ == '__main__':
	main()
