import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import re
import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.utils.class_weight import compute_class_weight
from sklearn.model_selection import train_test_split

def preprocess_text(text, abbreviations):
    text = text.lower()
    text = re.sub(r'[_;,\-\.\*]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    for abbr, full_text in abbreviations.items():
        text = re.sub(fr'\b{abbr}\b', full_text, text)
    text = text.strip()
    return text

def compute_embeddings(texts):
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    return embed(texts)

def main():
    # Load, preprocess and split data
    abbreviations = pd.read_parquet('0_data/abbreviations.parquet')
    data = pd.read_parquet('0_data/data.parquet')
    processed_texts = [preprocess_text(text, dict(zip(abbreviations['abbreviation'], abbreviations['full text']))) for text in data['desc']]
    X_train, X_val, y_train, y_val, _, unprocessed_X_val = [np.array(a) for a in train_test_split(processed_texts, data['control'], data['desc'], test_size=0.1, stratify=data['control'])]
    
    # Compute embeddings
    X_train_embed = compute_embeddings(X_train)
    X_val_embed = compute_embeddings(X_val)

    # Handle class imbalance
    class_weights = compute_class_weight('balanced', classes=np.array([0, 1]), y=y_train)

    # Add EarlyStopping callback
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=50, restore_best_weights=True)

    # Create, compile, train and save model
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(X_train_embed.shape[1],), dtype=tf.float32),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Dense(16, activation='elu'),
        tf.keras.layers.Dense(1, activation='sigmoid', kernel_regularizer=tf.keras.regularizers.l1_l2(l1=0.001, l2=0.001))
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(X_train_embed, y_train, epochs=10000, batch_size=64, class_weight=dict(enumerate(class_weights)), validation_data=(X_val_embed, y_val), callbacks=[early_stopping])
    model.save('1_model/classifier.keras')
    pd.DataFrame({'desc': unprocessed_X_val, 'control': y_val}).to_csv('1_model/data_val.csv', index=False)

if __name__ == '__main__':
    main()
