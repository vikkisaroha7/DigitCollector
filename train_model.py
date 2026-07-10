import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import Adam
import os


def train_model(epochs=5, batch_size=64, learning_rate=0.001):

    # ----------------------------------------
    # Load MNIST Dataset
    # ----------------------------------------
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    # ----------------------------------------
    # Normalize
    # ----------------------------------------
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    # ----------------------------------------
    # Reshape
    # ----------------------------------------
    x_train = x_train.reshape(-1, 28, 28, 1)
    x_test = x_test.reshape(-1, 28, 28, 1)

    # ----------------------------------------
    # Build CNN Model
    # ----------------------------------------
    model = models.Sequential([

        layers.Input(shape=(28, 28, 1)),

        layers.Conv2D(
            filters=32,
            kernel_size=(3, 3),
            activation="relu"
        ),

        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(
            filters=64,
            kernel_size=(3, 3),
            activation="relu"
        ),

        layers.MaxPooling2D((2, 2)),

        layers.Flatten(),

        layers.Dense(
            128,
            activation="relu"
        ),

        layers.Dropout(0.5),

        layers.Dense(
            10,
            activation="softmax"
        )

    ])

    # ----------------------------------------
    # Compile
    # ----------------------------------------
    optimizer = Adam(
        learning_rate=learning_rate
    )

    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    # ----------------------------------------
    # Train
    # ----------------------------------------
    history = model.fit(
        x_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.1,
        verbose=1
    )

    # ----------------------------------------
    # Evaluate
    # ----------------------------------------
    test_loss, test_accuracy = model.evaluate(
        x_test,
        y_test,
        verbose=0
    )

    # ----------------------------------------
    # Save Model
    # ----------------------------------------
    os.makedirs("models", exist_ok=True)

    model.save("models/digit_model.keras")

    return {
        "history": history.history,
        "accuracy": test_accuracy,
        "loss": test_loss
    }


if __name__ == "__main__":

    result = train_model()

    print(f"Accuracy : {result['accuracy']:.4f}")
    print(f"Loss : {result['loss']:.4f}")