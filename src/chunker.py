


def chunk_bible(file_path):
    verses = []
    with open(file_path, 'r') as file:
        for line in file[1:]:
                # Split the line at the first tab to separate the reference and the text
                reference, text = line.split("\t", 1)
                verses.append((reference.strip(), text.strip()))
    return verses


