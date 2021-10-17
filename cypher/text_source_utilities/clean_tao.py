with open('../text_sources/taoteching_original.txt', 'r') as f:
    new = []
    section = []
    for line in f.readlines():
        s_line = line.strip()
