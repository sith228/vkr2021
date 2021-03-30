import numpy as np


class RecognitionUtils(object):
    # correct solution:
    @staticmethod
    def __softmax(x):
        """
        Compute softmax values for each sets of scores in x
        :param x: argument
        :return: softmax function value for x argument
        """
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)  # only difference

    @staticmethod
    def decode_sequence(prob):
        # TODO: Add docstring
        symbols = '0123456789abcdefghijklmnopqrstuvwxyz '
        sequence = ''
        seq_p = []
        prev_pad = False
        for pos in prob.reshape(30, 37):
            s = RecognitionUtils.__softmax(pos)
            idx = np.argmax(pos)
            symbol = symbols[idx]
            if symbol != ' ':
                if sequence == '' or prev_pad or (sequence != '' and symbol != sequence[-1]):
                    prev_pad = False
                    sequence += symbols[idx]
                    seq_p.append(s[idx])
            else:
                prev_pad = True
        return sequence, seq_p