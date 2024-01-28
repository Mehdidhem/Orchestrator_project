import os
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.callbacks import TensorBoard
from datetime import datetime

# script lancé sur le serveur distant 
# juste pour la simulation, 
# et on utilise ici date et heure pour lid dexpereience


experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")

try:
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

   
    with tf.device('/cpu:0'):
        model = Sequential([
            Flatten(input_shape=(28, 28)),
            Dense(128, activation='relu'),
            Dense(10, activation='softmax')
        ])

    
    model.compile(optimizer='sgd',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    
    log_dir = os.path.join('/root/logs/tensorboard_logs', experiment_id)
    os.makedirs(log_dir, exist_ok=True)

    
    tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

   
    with tf.device('/cpu:0'):
        model.fit(x_train, y_train, epochs=50, validation_data=(x_test, y_test), callbacks=[tensorboard_callback])

    
    model_save_path = os.path.join('/root/models', f'{experiment_id}.h5')
    model.save(model_save_path)

except Exception as e:
    print(f"An error occurred: {e}")
