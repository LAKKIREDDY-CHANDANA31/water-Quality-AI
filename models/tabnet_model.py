from pytorch_tabnet.tab_model import TabNetClassifier


def build_tabnet_model():

    model = TabNetClassifier(
        n_d=16,
        n_a=16,
        n_steps=5,
        gamma=1.5,
        lambda_sparse=1e-4,
        optimizer_params=dict(lr=2e-2),
        verbose=1
    )

    return model