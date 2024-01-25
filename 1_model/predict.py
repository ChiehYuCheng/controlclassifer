import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import sys
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from train import preprocess_text

def classify_string(input_string):
    abbreviations = pd.read_parquet(os.path.join(os.path.dirname(__file__), '..', '0_data', 'abbreviations.parquet'))
    processed_text = preprocess_text(input_string, dict(zip(abbreviations['abbreviation'], abbreviations['full text'])))
    model = tf.keras.models.load_model(os.path.join(os.path.dirname(__file__), 'classifier.keras'))
    return model.predict(hub.load('https://tfhub.dev/google/universal-sentence-encoder/4')([processed_text]))[0][0]

def main(input):
    classification = classify_string(input)
    print(f'The probability of this item being export control is: {classification * 100:.2f}%')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input = sys.argv[1]
        print(f'Input provided: {input}')
    else:
        input = 'Inverter for Energytransformation in an E Motor'
        print(f'No input provided, using default: {input}')
    main(input)