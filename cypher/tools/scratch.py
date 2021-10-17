def set_source_file(self, file=''):
    non_empty_lines = 0
    if file[:-4] == '.txt':
        try:
            with open(file, 'r') as source_file:
                lines = source_file.readlines()
                stripped_lines = []
                for line in lines:
                    stripped = line.strip()
                    stripped_lines.append(stripped)
                    if len(stripped) > 0:
                        non_empty_lines += 1
                if non_empty_lines == 0:
                    raise ValueError('Source file is blank')
                self.plaintext = '\n'.join(lines)
            self.plaintext_file = file
        except Exception as e:
            print(f'There was an error reading the source file.')
            print(f'Error: {e}')
    else:
        raise ValueError('Source file must be a text file (.txt)')
