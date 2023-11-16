# ----------------------imports-----------------------------
import streamlit as st
import json
from streamlit_lottie import st_lottie 
import csv
import pandas as pd
import os
import subprocess
import time
# from folder_copy import copy_and_rename_folder
from cacheClear import cacheClear
import shutil
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import classification_report
import joblib
import pickle

import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ----------------------------------------------------------

# ---------------------custom modes-------------------------


# Define the base folder for storing the output binaries on the Desktop
output_base_folder = os.path.expanduser("~/Desktop/MalwareScannerActions")

# Define the subfolders for Skip, Remove, and Quarantine
output_skip_folder = os.path.join(output_base_folder, "Skip")
output_remove_folder = os.path.join(output_base_folder, "Remove")
output_quarantine_folder = os.path.join(output_base_folder, "Quarantine")

# Ensure the output folders exist, or create them if they don't
os.makedirs(output_skip_folder, exist_ok=True)
os.makedirs(output_remove_folder, exist_ok=True)
os.makedirs(output_quarantine_folder, exist_ok=True)
# Dictionary to track the state of each item (Skip, Remove, Quarantine)
item_states = {}

st.set_page_config(layout="wide", page_title="Results", page_icon="📊")

css_changes = """ 
        <style>
        #MainMenu, footer {visibility: hidden;}
        ul {list-style: none; padding-right: 0;}
        .css-1oe5cao1{position:relative; right:40px}
        .modebar-group {visibility: hidden;}
        .css-q8sbsg.e1nzilvr4 p {font-size: 22px; /* expander label font size adjustment */}
        

        .list-container, .css-k7vsyb {padding: 20px 2px 2px 2px;}


        </style>
        """
#Hide Streamlit pre-built items
st.markdown(css_changes, unsafe_allow_html=True)




# -------------------------functions------------------------------


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
def read_first_5_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines[:10]


# ---------------------------------------------------------------

# ---------------------------sidebar-----------------------------
with st.sidebar:
        
    # st.title("📄More Pages:")
    # st.markdown(pages, unsafe_allow_html=True) #pages
    # st.divider()
    # st.subheader("Clear cache")
    if st.button('Clear cache', key='clear_cache', type="primary", use_container_width=True):
        cacheClear()

    st.divider()
    st.subheader(":1234: Version ***(Beta)***")
    st.code("0.0.1")

# ---------------------------------------------------------------- 

# --------------------------contents------------------------------

st.title("📜 Analysis Report")


col1, col2 = st.columns([2,1])

with col1:
    st.subheader("Samples Identification:")
    # st.write("***Expand to see detailed report of specific malware.")
    #st.write(f"**Based on your selected classifier.**")
with col2:
    # path of json file of animated icon
    result_anim = load_lottiefile("/var/LearnStreamlit/assets/results.json")
    st_lottie(
        result_anim,
        speed=0.8,
        reverse=False,
        loop=True,
        quality="high",
        height=170,
        width=530,
        key=None
    )


df_1 = pd.read_csv("/var/LearnStreamlit/ml/GUI_dll.csv" )
df_2 = pd.read_csv("/var/LearnStreamlit/ml/GUI_system_call.csv" )

df_2['malwares'] = df_2['malwares'].str.replace(r'\d+', '')
df_1 = df_1.drop(['malwares'], axis = 1)

df = pd.concat([df_1,df_2], axis = 1)

class_counts = df['malwares'].value_counts()
# class_counts

xlab = np.unique(df['malwares'])

X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, 0:-1], df.iloc[:, -1], train_size=0.70, test_size=0.30, random_state=1)

testing_dataset = pd.concat([X_test, y_test], axis = 1)
training_dataset = pd.concat([X_train, y_train], axis = 1)

testing_dataset.to_csv("/var/LearnStreamlit/uploaded/testing_dataset.csv", index = False)
training_dataset.to_csv("/var/LearnStreamlit/ml/training_dataset.csv", index =   False)

# y_test

scaler = MinMaxScaler() 
X = scaler.fit_transform(X_train) 

model = RandomForestClassifier(n_estimators=2,max_depth=3,min_samples_split=3,min_samples_leaf=3)

class_counts = y_train.value_counts()
# class_counts


encoder = LabelEncoder()
y_train = encoder.fit_transform(y_train)
y_test = encoder.fit_transform(y_test)

model.fit(X_train, y_train)

# model

predictions = model.predict(X_test)
predictions_training = model.predict(X_train)

train_accuracy = accuracy_score(y_train, predictions_training)
train_f1 = f1_score(y_train, predictions_training, average='weighted')
print('Train time accuracy: ', "%.2f" % (train_accuracy*100))
print('Train time f1: ', "%.2f" % (train_f1*100))

accuracy = accuracy_score(y_test, predictions)
f1 = f1_score(y_test, predictions, average='weighted')
print('Test time accuracy: ', "%.2f" % (accuracy*100))
print('Test time f1: ', "%.2f" % (f1*100))

predictions = encoder.inverse_transform(predictions)
y_test_labels = encoder.inverse_transform(y_test)
y_train_labels = encoder.inverse_transform(y_train)


cm = confusion_matrix(y_test_labels, predictions)
cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

# We will store the results in a dictionary for easy access later
per_class_accuracies = {}

# Calculate the accuracy for each one of our classes
for idx, cls in enumerate(xlab):
    # True negatives are all the samples that are not our current GT class (not the current row) 
    # and were not predicted as the current class (not the current column)
    true_negatives = np.sum(np.delete(np.delete(cm, idx, axis=0), idx, axis=1))
    
    # True positives are all the samples of our current GT class that were predicted as such
    true_positives = cm[idx, idx]
    
    # The accuracy for the current class is the ratio between correct predictions to all predictions
    per_class_accuracies[cls] = round(((true_positives + true_negatives) / np.sum(cm)),3)
    print(f'Accuracy for {cls} : {per_class_accuracies[cls]}')

# Build the plot
plt.figure(figsize=(5, 2))
# sns.set(font_scale=1.4)
sns.heatmap(cm, annot=True, annot_kws={'size':10}, cmap="Blues", linewidths=0.2, xticklabels = xlab)

# Add labels to the plot
tick_marks = np.arange(len(xlab))
tick_marks2 = tick_marks + 0.5
# plt.xticks(tick_marks, xlab, rotation=25)
plt.yticks(tick_marks2, xlab, rotation=0)
plt.xlabel('Predicted Family')
plt.ylabel('Actual Family')
plt.title('Confusion Matrix for Decision Tree')
plt.show()


def get_tpr_fnr_fpr_tnr(cm, xlab):
    """
    This function returns class-wise TPR, FNR, FPR & TNR
    [[cm]]: a 2-D array of a multiclass confusion matrix
            where horizontal axes represent actual classes
            and vertical axes represent predicted classes
    [[clas
    
    s_names]]: a list containing the class names in the same order as in the confusion matrix
    {output}: a DataFrame of class-wise accuracy parameters with corresponding class names
    """
    dict_metric = dict()
    n = len(cm[0])
    row_sums = cm.sum(axis=1)
    col_sums = cm.sum(axis=0)
    array_sum = sum(sum(cm))
    
    # initialize a blank nested dictionary
    for i in range(1, n+1):
        keys = str(i)
        dict_metric[keys] = {"TPR":0, "FNR":0, "FPR":0, "TNR":0}
    
    # calculate and store class-wise TPR, FNR, FPR, TNR
    for i in range(n):
        for j in range(n):
            if i == j:
                keys = str(i+1)
                tp = cm[i, j]
                fn = row_sums[i] - cm[i, j]
                dict_metric[keys]["TPR"] = tp / (tp + fn)
                dict_metric[keys]["FNR"] = fn / (tp + fn)
                fp = col_sums[i] - cm[i, j]
                tn = array_sum - tp - fn - fp
                dict_metric[keys]["FPR"] = fp / (fp + tn)
                dict_metric[keys]["TNR"] = tn / (fp + tn)
    
    # Create DataFrame with class names as index
    df = pd.DataFrame(dict_metric).transpose()
    df.index = xlab
    
    return df

tpr_df = round(get_tpr_fnr_fpr_tnr(cm, xlab),3)
# tpr_df


round((tpr_df.iloc[:,0:].apply(np.mean)*100),2)



with st.expander("Uploaded Data:", expanded=True):
    df

with st.expander("Evaluation Metrics:", expanded=True):
    tpr_df = pd.DataFrame(tpr_df).transpose()
    st.table(tpr_df)


with st.expander("Testing Classification Report:", expanded=True):
    # Set the maximum height of the content
    
    # Display the table inside the expander
    # st.write("Testing Classification Report")
    # st.write(classification_report(y_test_labels, predictions, zero_division=1))
    classification_rep = classification_report(y_test_labels, predictions, zero_division=1, output_dict=True)
    classification_df = pd.DataFrame(classification_rep).transpose()
    st.table(classification_df)


with st.expander("Confusion Matrix:", expanded=True):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

# --------------------------------------------------------------------
