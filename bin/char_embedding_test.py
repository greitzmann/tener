#!/usr/bin/env python

import sys

sys.path.insert(0, "/opt/vlab/tener/src/")
import numpy as np
import tensorflow as tf
print(sys.path)

from tener.models.embeddings.character_embd import TransformerCharEncoding
from tener.misc.pretty_print import print_info

logger = tf.get_logger()
logger.setLevel("INFO")

def keras_tokenize(text_corpus, char_level=False, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'):
    lang_tokenizer = tf.keras.preprocessing.text.Tokenizer(filters=filters, oov_token="<UNK>", char_level=char_level, lower=False)
    lang_tokenizer.fit_on_texts(text_corpus)
    return lang_tokenizer


if __name__ == '__main__':
    text_data = ["4. Kurt Betschart - Bruno Risi ( Switzerland ) 22",
                 "Israel approves Arafat 's flight to West Bank .",
                 "Moreau takes bronze medal as faster losing semifinalist .",
                 "W D L G / F G / A P",
                 "-- Helsinki newsroom +358 - 0 - 680 50 248",
                 "M'bishi Gas sets terms on 7-year straight ."]
    text_char_tonkenizer = keras_tokenize(text_data, char_level=True)

    # split the text by spaces i.e list of list of words
    char_data = [text.split(" ") for text in text_data]

    MAX_SEQ_LENGTH = 12
    char_data_encoded = []
    for char_seq in char_data:
        print_info(">>> {}".format(len(char_seq)))
        # get_keras_tokenizer each sentence
        res = text_char_tonkenizer.texts_to_sequences(char_seq)
        # pad it
        res = tf.keras.preprocessing.sequence.pad_sequences(res, padding="post", maxlen=10)
        # group it as a batch
        res = np.array(res)
        res = np.pad(res, ((0, MAX_SEQ_LENGTH-len(char_seq)), (0, 0)), 'constant', constant_values=(0))
        # print_info(res.shape)
        char_data_encoded.append(res)


    vocab = list(text_char_tonkenizer.index_word.values())
    print_info(vocab)

    encoder = TransformerCharEncoding(char_emd_dim=128, len_char_vocab=vocab, d_model=128)

    char_data_encoded = np.array(char_data_encoded)
    print_info(char_data_encoded.shape)
    char_data_encoded = tf.convert_to_tensor(char_data_encoded)
    encoded = encoder(char_data_encoded)
    print_info(encoded)



