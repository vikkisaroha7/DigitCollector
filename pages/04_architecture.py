import streamlit as st
import tensorflow as tf

st.set_page_config(
    page_title="CNN Architecture",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 CNN Architecture")

# ---------------------------------------
# Load Model
# ---------------------------------------

try:
    model = tf.keras.models.load_model("models/digit_model.keras")
except Exception as e:
    st.error(f"Unable to load model.\n\n{e}")
    st.stop()

# ---------------------------------------
# Model Summary
# ---------------------------------------

st.subheader("Model Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Layers", len(model.layers))

with col2:
    st.metric("Parameters", f"{model.count_params():,}")

with col3:
    st.metric("Output Classes", 10)

st.divider()

# ---------------------------------------
# Layer Details
# ---------------------------------------

st.subheader("Layer Details")

for i, layer in enumerate(model.layers):

    with st.expander(f"Layer {i+1} : {layer.name}", expanded=False):

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Layer Type**")
            st.success(layer.__class__.__name__)

            st.write("**Trainable**")
            st.info(layer.trainable)

        with col2:

            st.write("**Parameters**")
            st.success(f"{layer.count_params():,}")

        # Output Shape
        try:
            st.write("**Output Shape**")
            st.code(str(layer.output.shape))
        except:
            pass

        # Configuration
        st.write("**Configuration**")

        config = layer.get_config()

        st.json(config)

st.divider()

# ---------------------------------------
# CNN Flow Diagram
# ---------------------------------------

st.subheader("CNN Flow")

st.info(
"""
Input Image (28×28×1)

⬇️

Conv2D (32 Filters)

⬇️

MaxPooling2D

⬇️

Conv2D (64 Filters)

⬇️

MaxPooling2D

⬇️

Flatten

⬇️

Dense (128)

⬇️

Dropout (0.5)

⬇️

Dense (10)

⬇️

Softmax Output
"""
)

st.divider()

# ---------------------------------------
# Keras Summary
# ---------------------------------------

st.subheader("Keras Model Summary")

summary = []

model.summary(print_fn=lambda x: summary.append(x))

st.code("\n".join(summary))