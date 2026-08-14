import tensorflow as tf
from tensorflow.keras import layers, Model


class FTTransformer(Model):

    def __init__(
        self,
        num_features,
        d_token=32,
        num_heads=4,
        num_layers=3,
        dropout=0.2
    ):
        super().__init__()

        self.num_features = num_features
        self.d_token = d_token

        # ----------------------------------------------------
        # Convert each numerical feature into a token
        # ----------------------------------------------------
        self.feature_embedding = layers.Dense(d_token)

        # ----------------------------------------------------
        # Transformer blocks
        # ----------------------------------------------------
        self.transformer_blocks = []

        for _ in range(num_layers):

            self.transformer_blocks.append(
                {
                    "norm1": layers.LayerNormalization(),

                    "attention": layers.MultiHeadAttention(
                        num_heads=num_heads,
                        key_dim=d_token // num_heads,
                        dropout=dropout
                    ),

                    "dropout1": layers.Dropout(dropout),

                    "norm2": layers.LayerNormalization(),

                    "ffn": tf.keras.Sequential(
                        [
                            layers.Dense(
                                d_token * 2,
                                activation="gelu"
                            ),

                            layers.Dropout(dropout),

                            layers.Dense(d_token)
                        ]
                    ),

                    "dropout2": layers.Dropout(dropout)
                }
            )

        # ----------------------------------------------------
        # Final normalization
        # ----------------------------------------------------
        self.norm = layers.LayerNormalization()

        # ----------------------------------------------------
        # Classification head
        # ----------------------------------------------------
        self.classifier = tf.keras.Sequential(
            [
                layers.Dense(
                    64,
                    activation="relu"
                ),

                layers.Dropout(dropout),

                layers.Dense(
                    32,
                    activation="relu"
                ),

                layers.Dropout(dropout),

                layers.Dense(
                    1,
                    activation="sigmoid"
                )
            ]
        )

    def call(self, inputs, training=False):

        # Input:
        # (batch_size, 9)

        # ----------------------------------------------------
        # Convert features into tokens
        # ----------------------------------------------------
        x = tf.expand_dims(
            inputs,
            axis=-1
        )

        # Shape:
        # (batch, 9, 1)
        #
        # -> (batch, 9, d_token)

        x = self.feature_embedding(x)

        # ----------------------------------------------------
        # Transformer blocks
        # ----------------------------------------------------
        for block in self.transformer_blocks:

            # ------------------------------
            # Self Attention
            # ------------------------------

            residual = x

            x_norm = block["norm1"](x)

            attention_output = block["attention"](
                x_norm,
                x_norm,
                training=training
            )

            attention_output = block["dropout1"](
                attention_output,
                training=training
            )

            x = residual + attention_output

            # ------------------------------
            # Feed Forward Network
            # ------------------------------

            residual = x

            x_norm = block["norm2"](x)

            ffn_output = block["ffn"](
                x_norm,
                training=training
            )

            ffn_output = block["dropout2"](
                ffn_output,
                training=training
            )

            x = residual + ffn_output

        # ----------------------------------------------------
        # Final normalization
        # ----------------------------------------------------
        x = self.norm(x)

        # ----------------------------------------------------
        # Global average pooling
        # ----------------------------------------------------
        x = tf.reduce_mean(
            x,
            axis=1
        )

        # ----------------------------------------------------
        # Classification
        # ----------------------------------------------------
        return self.classifier(
            x,
            training=training
        )