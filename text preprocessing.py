import os, sys

# init vocabulary size
voc_size = 30

# Reading Corpus File
def read_corpus_file(file_path):
    words_list = []
    # read corpus file
    # and build the word list
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        for line in file_handle:
            words = line.strip().split()
            for word in words:
                words_list.append(word.strip())
    return words_list

# Get Unique word list
def get_unique_wordlist(words_list):
    unique_words_list = list(set(words_list))
    return unique_words_list

# Compute the frequency of each word in the corpus
def compute_word_frequency(words_list, unique_words_list):
    word_freq = []
    for w in unique_words_list:
        word_freq.append((w, words_list.count(w)))
    return word_freq

# Append a special symbol to the end of every word in the dataset
def append_symbol(word_freq, symbol):
    appended_list = []
    for word in word_freq:
        appended_list.append((word[0] + symbol, word[1]))
    return appended_list

# split word
def split_word(word, suffix):
    char_list = list(word)
    if suffix is None:
        return char_list
    else:
        char_list.append(suffix)
        return char_list

# splitted word vocabulary
def get_splitted_vocabulary(word_freq, symbol):
    splitted_vocabulary = []
    for w, freq in word_freq:
        item = split_word(w, symbol)
        splitted_vocabulary.append([item, freq])
    return splitted_vocabulary
# initialize vocabulary
def init_vocabulary(word_freq):
    init_voc = []
    for w, freq in word_freq:
        characters = w.split()
        init_voc += characters
        init_voc = list(set(init_voc))
    return init_voc

# compute pairs frequency
def get_pair_freq(word_freq):
    pairs = {}
    for w, freq in word_freq:
        characters = w.split()
        for i in range(len(characters) - 1):
            pair = (characters[i], characters[i + 1])
            cur_freq = pairs.get(pair, 0)
            pairs[pair] = cur_freq + freq
    return pairs
# convert list of characters in vocabulary to string splitted by space
# format ['a', 'b'] => ['a b']
def convert_list2str_vocabulary(word_freq):
    voc = []
    for w, freq in word_freq:
        voc.append([" ".join(w), freq])
    return voc

def merge_vocabulary(vocabulary, most_pair):
    new_vocabulary = []
    old = " ".join(list(most_pair))
    new = "".join(list(most_pair))
    for word, freq in vocabulary:
        new_word = word.replace(old, new)
        new_vocabulary.append([new_word, freq])
    return new_vocabulary

def get_pairs(word):
    pairs = set()
    pre_char = word[0]
    for char in word[1:]:
        pairs.add((pre_char, char))
        pre_char = char

    return pairs

# find the pair from bpe operations
# e.g. find a pair ('e', 's') from bpe operstions {('l', 'o'), ('e', 's'), ('es', 't')}
def find_bpe_operation(pairs, bpe_operations):
    matched_pair = ()
    for i, bpe in enumerate(bpe_operations):
        for pair in pairs:
            if bpe == pair:
                matched_pair = bpe
                return matched_pair, i
    return matched_pair, -1

# merge pair in character list
# e.g. ['l', 'o', 'w', 'e', 's', 't', '</w>'] => ['l', 'o', 'w', 'es', 't', '</w>']
def merge_word_by_pair(OOV_word, pair):
    word = " ".join(OOV_word)
    old = " ".join(list(pair))
    new = "".join(list(pair))
    new_word = word.replace(old, new)
    new_word = new_word.split()
    return new_word

def main():
    
    # Part-1
    file_name = 'corpus.txt'
    words_list = read_corpus_file(file_name)
    # print(words_list)

    # 1 a) Gate and prepare a training text dataset/corpus
    unique_words_list = get_unique_wordlist(words_list)
    print("\n")
    print("Reading dataset/corpus:")
    print("File Name : {}".format(file_name))
    print("Initial unique word list in the dataset:")
    print("Word List: [{}]".format(", ".join(unique_words_list)))

    print("\n")

    # 1 b) Compute the frequency of each word in the corpus
    word_freq = compute_word_frequency(words_list, unique_words_list)
    print('computing frequency:')
    print('Word frequency: [{}]'.format(", ".join([w[0] + " (" + str(w[1]) + ")" for w in word_freq])))

    print("\n")
    # 1 c) Define a required certain size of sub-word vocabulary
    print("Defining Vocabulary:")
    voc_size_str = input("Required vocabulary size:")
    try:
        voc_size = int(voc_size_str)
    except:
        print("Please input the integer value")
        sys.exit()
    
    print("\n")
    # 1 d) Append a special symbol to the end of every word in the dataset
    spec_symbol = '</w>'
    appended_list = append_symbol(word_freq, symbol = spec_symbol)
    print('Appending special symbol:')
    print('Appended symbol \'{}\':[{}]'.format(spec_symbol, ", ".join(['\'' + w + '\' - (' + str(freq) + ')' for w, freq in appended_list])))

    print("\n")
    # 1 e) Split each word in the corpus into sequence of characters
    print('Splitting words:')
    splitted_vocabulary = get_splitted_vocabulary(word_freq, spec_symbol)
    splitted_vocabulary = convert_list2str_vocabulary(splitted_vocabulary)
    print('Split words: [{}]'.format(", ".join(["\'" + w + '\' - (' + str(freq) + ')' for w, freq in splitted_vocabulary])))

    print("\n")
    # 2. Initialize the vocabulary with unique characters in the corpus
    print('Initializing vocabulary:')
    init_voc = init_vocabulary(splitted_vocabulary)
    print('Initial vocabulary:({}) - {}'.format(len(init_voc), init_voc))

    iter_number = 13

    bpe_operations = []
    for i in range(iter_number):
        # 3. Iteratively compute the frequency of a pair of characters or character sequences in the corpus

        print('Pairs frequency:')
        pairs = get_pair_freq(splitted_vocabulary)
        print(pairs)
        if not pairs:
            print(i)
            break
        print("\n")
        # Find the most frequent pair and merge them together into a new token.
        most_pair = max(pairs, key = pairs.get)
        print("The most frequent pair or best pair in the corpus: ", most_pair)

        print("\n")
        # 4. Merge the most frequent pair in corpus and save to the vocabulary
        print('Merging the most frequent pair:')
        merged_pair = "".join(list(most_pair))
        print('Merged pair:({})'.format(merged_pair))

        print("\n")
        # 5. Save the best pair to the vocabulary
        print('saving the most frequent pair:')
        # merged_vocabulary = 
        merged_vocabulary = merge_vocabulary(splitted_vocabulary, most_pair)
        print('Saved pair:{' + ", ".join(["\'" + w + "\'" + ":" + str(freq)  for w, freq in merged_vocabulary]) + "}")
        bpe_operations.append(most_pair)
        splitted_vocabulary = merged_vocabulary

    print("\n")
    print('Iterating until reaching the number of tokens size specified:')
    print('BPE Merg Operations:{}'.format(["".join(list(item)) for item in bpe_operations]))

    # End of Part-1

    # Part-2 Applying BPE to an OOV word or new vocabulary

    known_word = 'newest'
    unknown_word =  'fastest!'

    print("\n")
    # 1. Split the OOV word into characters after appending </w>
    OOV_word = split_word(known_word, spec_symbol)
    print("Appending </w> and splitting OOV word:")
    print('OOV (original word) = \'{}\''.format(known_word))
    print('</w> appended:[\'{}\']'.format(''.join(OOV_word)))
    print('OOV word split:', OOV_word)

    print("\n")
    # 2. Compute pair of character or character sequences in a word
    print("Computing pair of character in the word:")
    pairs = get_pairs(OOV_word)
    print('Computed pairs:', pairs)

    print("\n")
    # 3. Select the pairs present in the learned operations
    selected_pair, index = find_bpe_operation(pairs, bpe_operations)
    print('Selecting the pairs:', selected_pair)

    print("\n")
    # 4. Merge the most frequent pair (Apply the merge on the word)
    print("Merging the most frequent pair")
    new_OOV_word = merge_word_by_pair(OOV_word, selected_pair)
    print('Merged pair:', new_OOV_word)

    print("\n")
    # 5. Repeat steps 2 and 3, 4 until merging is possible.

    cur_bpe_operations = []
    OOV_word = split_word(unknown_word, spec_symbol)
    while True:
        # 1. Split the OOV word into characters after appending </w>
        print("Appending </w> and splitting OOV word:")
        print('OOV (original word) = \'{}\''.format(unknown_word))
        print('</w> appended:[\'{}\']'.format(''.join(OOV_word)))
        print('OOV word split:', OOV_word)

        print("\n")
        # 2. Compute pair of character or character sequences in a word
        print("Computing pair of character in the word:")
        pairs = get_pairs(OOV_word)
        print('Computed pairs:', pairs)

        print("\n")
        # 3. Select the pairs present in the learned operations
        selected_pair, index = find_bpe_operation(pairs, bpe_operations)
        if not selected_pair:
            break
        print('Selecting the pairs:', selected_pair)

        print("\n")
        # 4. Merge the most frequent pair (Apply the merge on the word)
        print("Merging the most frequent pair")
        new_OOV_word = merge_word_by_pair(OOV_word, selected_pair)
        print('Merged pair:', new_OOV_word)
        bpe_operations.append((new_OOV_word, index))

        OOV_word = new_OOV_word
    print(new_OOV_word)
if __name__ == '__main__':
    main()
