# -*- coding: utf-8 -*-
"""DataPreprocessor.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ESg5bpna8aIdfJHYODiEDsJBV5DzjaAQ
"""

from IPython.display import Markdown, display

display(Markdown("""
# 🛠️ Module 2: Data Preprocessor

**Purpose:** This module allows you to upload a dataset (typically a CSV file from a data loading/validation step) and apply various common preprocessing techniques to prepare it for machine learning.

**How it fits in a workflow:**
This module usually follows a "Data Loader & Validator". The preprocessed data output from this module can then be passed to a "Model Trainer" module.

**Functionality:**
1.  **Upload CSV Data:** Upload the dataset you want to preprocess.
2.  **Select Columns:** Identify columns for specific preprocessing tasks.
3.  **Missing Value Imputation:**
    * Choose strategies for numerical columns (mean, median).
    * Choose strategies for categorical columns (mode, constant fill).
4.  **Categorical Feature Encoding:**
    * Apply One-Hot Encoding or Label Encoding to selected categorical columns.
5.  **Numerical Feature Scaling:**
    * Apply StandardScaler or MinMaxScaler to selected numerical columns.
6.  **Preview Changes:** See the impact of transformations (e.g., view updated DataFrame head).
7.  **Download Processed Data:** Download the transformed dataset as a CSV or Pickle file.

**Order of Operations:** Preprocessing steps are generally applied in this order:
1. Missing Value Imputation
2. Categorical Encoding
3. Numerical Scaling (on numerical columns, including those newly created by one-hot encoding if applicable)
"""))

print("Installing/checking libraries...")
!pip install -q pandas numpy scikit-learn ipywidgets

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

import ipywidgets as widgets
from ipywidgets import VBox, HBox, Layout
from IPython.display import display, clear_output, FileLink
import io
import pickle

print("\nLibraries ready!")

# --- Global variables ---
df_original = None # Stores the initially loaded dataframe
df_processed = None # Stores the dataframe after processing steps
output_main_preprocess = widgets.Output() # Main output area
column_details_output = widgets.Output()

# --- UI Element Definitions ---
style = {'description_width': 'initial'}
l_auto = Layout(width='auto')
l_full = Layout(width='100%')
l_95width = Layout(width='95%')
l_48width = Layout(width='48%', margin='0 1% 0 1%') # For side-by-side elements

# --- 1. File Uploader ---
file_uploader_preprocess = widgets.FileUpload(
    accept='.csv', multiple=False, description='Upload Raw CSV:', style=style)

# --- 2. Column Selectors (populated after upload) ---
all_columns_preprocess = []
numerical_cols_widget = widgets.SelectMultiple(description="Numerical Cols:", disabled=True, rows=5, style=style)
categorical_cols_widget = widgets.SelectMultiple(description="Categorical Cols:", disabled=True, rows=5, style=style)

# --- 3. Missing Value Imputation ---
num_impute_strategy = widgets.Dropdown(options=['mean', 'median', 'None'], value='mean', description='Num Impute:', style=style)
cat_impute_strategy = widgets.Dropdown(options=['most_frequent', 'constant', 'None'], value='most_frequent', description='Cat Impute:', style=style)
cat_impute_constant = widgets.Text(value='missing', description='Fill Constant:', disabled=True, style=style)

# --- 4. Categorical Encoding ---
cat_encoding_cols_selector = widgets.SelectMultiple(description="Encode These Cat Cols:", disabled=True, rows=3, style=style)
cat_encoding_method = widgets.RadioButtons(options=['One-Hot Encode', 'Label Encode', 'None'], value='None', description='Encoding Method:', style=style)

# --- 5. Numerical Scaling ---
num_scaling_cols_selector = widgets.SelectMultiple(description="Scale These Num Cols:", disabled=True, rows=3, style=style)
num_scaling_method = widgets.RadioButtons(options=['StandardScaler', 'MinMaxScaler', 'None'], value='None', description='Scaling Method:', style=style)

# --- 6. Action Button & Output ---
preprocess_button = widgets.Button(description="Apply Preprocessing", button_style='primary', icon='cogs', disabled=True)
download_csv_button = widgets.Button(description="Download Processed CSV", button_style='info', icon='download', disabled=True, layout=l_auto)
download_pickle_button = widgets.Button(description="Download Processed Pickle", button_style='info', icon='download', disabled=True, layout=l_auto)
data_preview_processed = widgets.Output(layout=Layout(height='250px', overflow_y='auto', border='1px solid lightgray', margin='5px 0 0 0'))


# --- Helper function to update column selectors ---
def update_column_selectors_and_widgets():
    global df_original, all_columns_preprocess
    if df_original is None:
        numerical_cols_widget.options = []
        categorical_cols_widget.options = []
        cat_encoding_cols_selector.options = []
        num_scaling_cols_selector.options = []
        numerical_cols_widget.disabled = True
        categorical_cols_widget.disabled = True
        cat_encoding_cols_selector.disabled = True
        num_scaling_cols_selector.disabled = True
        preprocess_button.disabled = True
        return

    all_columns_preprocess = df_original.columns.tolist()
    num_cols = df_original.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df_original.select_dtypes(include=['object', 'category']).columns.tolist()

    numerical_cols_widget.options = all_columns_preprocess
    numerical_cols_widget.value = [col for col in num_cols if col in all_columns_preprocess] # Pre-select detected num cols
    categorical_cols_widget.options = all_columns_preprocess
    categorical_cols_widget.value = [col for col in cat_cols if col in all_columns_preprocess] # Pre-select detected cat cols

    cat_encoding_cols_selector.options = cat_cols
    cat_encoding_cols_selector.value = [] # User to select
    num_scaling_cols_selector.options = num_cols # Initially, only original numerical cols
                                                # This will be updated after one-hot encoding

    numerical_cols_widget.disabled = False
    categorical_cols_widget.disabled = False
    cat_encoding_cols_selector.disabled = False if cat_cols else True
    num_scaling_cols_selector.disabled = False if num_cols else True
    preprocess_button.disabled = False

    with column_details_output:
        clear_output(wait=True)
        display(Markdown("#### Detected Column Types (you can adjust selections below):"))
        display(HBox([numerical_cols_widget, categorical_cols_widget]))
        display(Markdown(f"**All Columns:** {', '.join(all_columns_preprocess)}"))
        display(Markdown(f"**Initially Detected Numerical:** {', '.join(num_cols)}"))
        display(Markdown(f"**Initially Detected Categorical:** {', '.join(cat_cols)}"))


# --- Event Handlers ---
def on_file_upload_preprocess(change):
    global df_original, df_processed
    with output_main_preprocess:
        clear_output(wait=True)
        display(Markdown("--- Loading Data ---"))
    with data_preview_processed:
        clear_output(wait=True)

    if change['new']:
        uploaded_file_info = change['owner'].value
        filename = list(uploaded_file_info.keys())[0]
        content = uploaded_file_info[filename]['content']
        try:
            df_original = pd.read_csv(io.BytesIO(content))
            df_processed = df_original.copy() # Start with a copy
            with output_main_preprocess:
                clear_output(wait=True)
                print(f"👍 Successfully loaded '{filename}'. Shape: {df_original.shape}.")
                display(Markdown("Original Data Preview (first 5 rows):"))
                display(df_original.head())
            update_column_selectors_and_widgets()
            download_csv_button.disabled = True # Re-disable download until processed
            download_pickle_button.disabled = True
        except Exception as e:
            df_original = None
            df_processed = None
            with output_main_preprocess:
                clear_output(wait=True)
                print(f"❌ Error loading or parsing CSV: {e}")
            update_column_selectors_and_widgets() # This will disable dependent widgets
    else:
        df_original = None
        df_processed = None
        with output_main_preprocess:
            clear_output(wait=True)
            print("File removed or no file uploaded.")
        update_column_selectors_and_widgets()

file_uploader_preprocess.observe(on_file_upload_preprocess, names='value')

def on_cat_impute_strategy_change(change):
    cat_impute_constant.disabled = (change['new'] != 'constant')
cat_impute_strategy.observe(on_cat_impute_strategy_change, names='value')
on_cat_impute_strategy_change({'new': cat_impute_strategy.value}) # Initialize

# --- Layout for UI sections ---
# Section Titles
title_upload = widgets.HTML("<h4>1. Upload Data to Preprocess</h4>")
title_column_config = widgets.HTML("<h4>2. Configure Column Types (Adjust if needed)</h4>")
title_imputation = widgets.HTML("<h4>3. Missing Value Imputation</h4>")
title_encoding = widgets.HTML("<h4>4. Categorical Feature Encoding</h4>")
title_scaling = widgets.HTML("<h4>5. Numerical Feature Scaling</h4>")
title_actions = widgets.HTML("<h4>6. Apply & Download</h4>")
title_preview = widgets.HTML("<h4>Processed Data Preview & Status:</h4>")


# Organize UI
imputation_box = VBox([
    title_imputation,
    HBox([num_impute_strategy, cat_impute_strategy]),
    cat_impute_constant
])
encoding_box = VBox([
    title_encoding,
    cat_encoding_cols_selector,
    cat_encoding_method
])
scaling_box = VBox([
    title_scaling,
    num_scaling_cols_selector,
    num_scaling_method
])
actions_box = VBox([
    title_actions,
    preprocess_button,
    HBox([download_csv_button, download_pickle_button], layout=Layout(justify_content='space-around', margin='10px 0 0 0'))
])

# Display UI
display(VBox([
    title_upload,
    file_uploader_preprocess,
    widgets.HTML("<hr>"),
    title_column_config,
    column_details_output, # For HBox of num/cat selectors & detected types
    widgets.HTML("<hr>"),
    HBox([imputation_box, encoding_box], layout=Layout(justify_content='space-between')), # Imputation and Encoding side-by-side
    widgets.HTML("<hr>"),
    scaling_box,
    widgets.HTML("<hr>"),
    actions_box,
    widgets.HTML("<hr>"),
    title_preview,
    data_preview_processed,
    output_main_preprocess
]))

# Initial call to set widget states if no file uploaded yet
if df_original is None:
    with output_main_preprocess: clear_output(); print("Awaiting CSV file upload for preprocessing...")
    update_column_selectors_and_widgets()

