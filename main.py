from preprocessing.clean_data import load_and_clean_data
from preprocessing.split_data import split_and_scale_data

# Load and clean data
data = load_and_clean_data()

# Split and scale data
X_train, X_test, y_train, y_test = split_and_scale_data(data)