import joblib
from keras.models import load_model
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import numpy as np



#                               <-----------Random Forest----------->

# def process_behaviour():
#     model = joblib.load(f"/var/LearnStreamlit/ml/DNN.joblib")
#     testing_df = pd.read_csv("/var/LearnStreamlit/analysis/preprocessing/csv/final_data.csv")

#     y_test = testing_df.iloc[:,0]
#     testing_df = testing_df.iloc[:,1:]

#     training_dataset = pd.read_csv("/var/LearnStreamlit/ml/training_dataset.csv")
#     y = training_dataset.iloc[:,-1]
#     training_dataset = training_dataset.iloc[:,:-2]
#     training_columns = training_dataset.columns

#     X = testing_df.iloc[:,:-1]
#     X = X.reindex(columns=training_columns, fill_value=0)
#     extra_columns = [col for col in X.columns if col not in training_columns]
#     X = X.drop(columns=extra_columns)

#     encoder = LabelEncoder()
#     y = encoder.fit_transform(y)

#     scaler = MinMaxScaler()
#     X = scaler.fit_transform(X)

#     predictions = model.predict(X)
#     predictions = encoder.inverse_transform(predictions)
#     print(predictions)

    # results = pd.DataFrame({'Executable_name': y_test, 'Prediction': predictions})
    # results.to_csv('/var/LearnStreamlit/analysis/results/csv/predictions.csv', index=False)
# <---------->

def process_behaviour():
    model = load_model("/var/LearnStreamlit/ml/model.h5")
    model.summary()
    testing_df = pd.read_csv("/var/LearnStreamlit/analysis/uploaded/testing_dataset.csv")
    y_test = testing_df.iloc[:,0]
    X = testing_df.iloc[:,1:]


    training_dataset = pd.read_csv("/var/LearnStreamlit/ml/training_dataset_DNN.csv" )
    y = training_dataset.iloc[:,-1]
    training_dataset = training_dataset.iloc[:,:-1]
    training_columns = training_dataset.columns


    X = X.reindex(columns=training_columns, fill_value=0)
    extra_columns = [col for col in X.columns if col not in training_columns]
    X = X.drop(columns=extra_columns)

    encoder = LabelEncoder()
    y = encoder.fit_transform(y)

    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)

    predictions = model.predict(X)
    predictions = np.argmax(predictions, axis=-1)
    predictions = encoder.inverse_transform(predictions)

    print(predictions)

    results = pd.DataFrame({'Executable_name': y_test, 'Prediction': predictions})
    results.to_csv('/var/LearnStreamlit/analysis/results/csv/predictions.csv', index=False)
