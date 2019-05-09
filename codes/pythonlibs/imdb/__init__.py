import os
import numpy as np
import re

def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'nt", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    #phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    phrase = re.sub(r" im ", " i am ", phrase)
    phrase = re.sub(r" id ", " i would ", phrase)
    return phrase


def read_files_from_folder(folder_path, max_files, extension='.txt', convert_fcn=lambda file: file.read()):

    file_path = folder_path + str('{}' if folder_path.endswith('/') else '/{}')
    result = []

    for i, filename in enumerate(os.listdir(folder_path)):


        if max_files > 0 and i >= max_files:
            break

        if filename.endswith(extension):
            with open(file_path.format(filename), 'r') as file:
                content = convert_fcn(file)

                result.append((filename, content))

    return result


def get_imdb_reviews_dataset(path, dataset_size=-1):
    '''
    Dataset download from: ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz
    :return: (train_set, test_set)
    '''
    path = path + str('{}/{}' if path.endswith('/') else '/{}/{}')

    assert dataset_size < 0 or dataset_size >= 4

    part_size = int(dataset_size/4)


    train_pos = read_files_from_folder(path.format('train', 'pos'), part_size)
    train_neg = read_files_from_folder(path.format('train', 'neg'), part_size)
    test_pos  = read_files_from_folder(path.format('test', 'neg'), part_size)
    test_neg  = read_files_from_folder(path.format('train', 'neg'), part_size)

    def npy_hstack(record, cls_vctr):
        phrase = decontracted(record[1].lower())
        phrase = re.sub('<.{,5}>', '', phrase)
        phrase = re.sub('[^a-zA-Z0-9 ]+', '', phrase)

        return np.hstack([
            np.asarray(phrase, dtype='str'),
            np.asarray(cls_vctr)
        ])

    train_pos = list(map(lambda t: npy_hstack(t, [1, 0]), train_pos))
    train_neg = list(map(lambda t: npy_hstack(t, [0, 1]), train_neg))
    test_pos  = list(map(lambda t: npy_hstack(t, [1, 0]), test_pos))
    test_neg  = list(map(lambda t: npy_hstack(t, [0, 1]), test_neg))

    train = np.vstack([np.vstack(train_pos), np.vstack(train_neg)])
    test = np.vstack([np.vstack(test_pos), np.vstack(test_neg)])

    np.random.shuffle(train)
    np.random.shuffle(test)

    return train, test

