with open('../text_sources/callofcthulhu_original.txt', encoding='utf8') as f:
    with open('../text_sources/callofcthulhu.txt', 'w+', encoding='utf8') as n:
        for line in f.readlines():
            n.write(line.strip())
            n.write('\n')
