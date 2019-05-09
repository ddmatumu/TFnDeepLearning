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
    '''
    Reads all of the files of the given extension from the target folder.
    
    :param folder_path target folder from which read the files
    :param max_files maximum number of files to read
    :param extension extension of the files to be read
    :param convert_fcn function to convert the files into strings
    '''

    file_path = folder_path + str('{}' if folder_path.endswith('/') else '/{}')
    result = []

    for i, filename in enumerate(os.listdir(folder_path)):


        if max_files > 0 and i >= max_files:
            break

        if filename.endswith(extension):
            # Added by Sonvx for encoding issue in Windows.
            try:
                with open(file_path.format(filename), 'r') as file:
                    content = convert_fcn(file)

                    result.append((filename, content))
            except:
                # TODO: handle encoding problem here.
                pass

    return result


def get_imdb_reviews_dataset(path='./aclImdb/', max_dataset_size=-1, trunc=-1):
    '''
    Dataset download from: ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz
    :param path the path at which the imdb dataset is
    :param max_dataset_size maximum number of rows of the dataset
    :param trunc maximum number of words for every review. Reviews get truncated after.
    :return (train_set, test_set). Every row is of 3 cells: (string, lbl_0, lbl_1)
    '''
    path = path + str('{}/{}' if path.endswith('/') else '/{}/{}')

    assert max_dataset_size < 0 or max_dataset_size >= 4

    part_size = int(max_dataset_size/4)
    


    train_pos = read_files_from_folder(path.format('train', 'pos'), part_size)
    train_neg = read_files_from_folder(path.format('train', 'neg'), part_size)
    test_pos  = read_files_from_folder(path.format('test', 'neg'), part_size)
    test_neg  = read_files_from_folder(path.format('train', 'neg'), part_size)

    
    def npy_hstack(record, cls_vctr):
        phrase = decontracted(record[1].lower())
        phrase = re.sub('<.{,5}>', '', phrase)
        phrase = re.sub('[^a-zA-Z0-9 ]+', '', phrase)
        
        if trunc > 0:
            phrase = phrase.split(' ')[:trunc]
            phrase = ' '.join(phrase)
        
        

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

    
    #np.random.shuffle(train)
    #np.random.shuffle(test)
    

    return (train[:, :-2], train[:,-2:]), (test[:, :-2], test[:, -2:])



