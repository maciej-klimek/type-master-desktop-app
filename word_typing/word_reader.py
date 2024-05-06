def read_words(filename):
    with open(filename, 'r') as file:
        words = file.readlines()
    return [word.strip() for word in words]