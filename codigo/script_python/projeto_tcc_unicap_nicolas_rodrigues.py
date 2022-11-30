# -*- coding: utf-8 -*-
"""Projeto TCC UNICAP Nicolas Rodrigues.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HsXAKJqx94hYPaw4lXQSK-EbPxt6loBY
"""

!pip install tensorflow==2.7.0

import pandas as pd
import numpy as np
import io
from google.colab import files
# tornar valores numpy mais fáceis de ler
np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras import regularizers
from sklearn.model_selection import train_test_split

# enviar dados em .csv
data = files.upload()

df = pd.read_csv(io.StringIO(data['data.csv'].decode('utf-8')))
df.head

# análise dos tipos de dados
df.dtypes

# definir objeto diag
diagnosis = df.diagnosis
# colocar diag no fim da tabela
df.drop('diagnosis', axis = 1, inplace = True)
df['diagnosis'] = diagnosis
df.head()

# descobrir qual a média de diagnósticos e mapear os strings para int (malígno - 1 ou benigno - 0 ?):
diagnosis_coder = {'M':1, 'B':0}
df.diagnosis = df.diagnosis.map(diagnosis_coder)
avgdiag = df["diagnosis"].mean()
df.head

nben = (df['diagnosis']==0).sum()
nmal=  (df['diagnosis']==1).sum()
ntot = ((df['diagnosis']==0).sum())+((df['diagnosis']==1).sum())

percben = (nben/ntot)*100
percmal = (nmal/ntot)*100

print(df['diagnosis'].value_counts())
print(ntot)
print(avgdiag)
print(percben)
print(percmal)

# separar os dados iniciais em 3 data sets (dados de treino, dados de validação e dados de teste)
#lembrar: features são os inputs, labels são os targets     x = features,  y = targets

# validação
train, test = train_test_split(df, test_size=0.2)
train, val = train_test_split(train, test_size=0.2)

from sklearn.preprocessing import Normalizer

# teste e treino - usar 80% para treino

# obs: x train = df_features y train = df_labels
X_train, X_test, y_train, y_test = train_test_split(df.iloc[:,:-1], df['diagnosis'], train_size = .8 )

# normalização
norm = Normalizer()
norm.fit(X_train)

X_train_norm = norm.transform(X_train)
X_test_norm = norm.transform(X_test)

#df_features = train.copy()
#df_labels = df_features.pop('diagnosis')
#df_labels = df_labels/avgdiag

val_features = val.copy()
val_labels = val.pop('diagnosis')
val_labels = val_labels/avgdiag

#test_features = test.copy()
#test_labels = test.pop('diagnosis')
#test_labels = test/avgdiag

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score

# Parameters
RF_params = {'n_estimators':[10,50,100, 200]}

# Instantiate RFC
RFC_2 = RandomForestClassifier(random_state=42)

# Instantiate gridsearch using RFC model and dictated parameters
RFC_2_grid = GridSearchCV(RFC_2, RF_params)

# Fit model to training data
RFC_2_grid.fit(X_train_norm, y_train)

# Print best parameters
print('Número optimizado de estimadores: {}'.format(RFC_2_grid.best_params_.values()))
# Train RFC on whole training set

# Instantiate RFC with optimal parameters
RFC_3 = RandomForestClassifier(n_estimators=50, random_state=42)

# Fit RFC to training data
RFC_3.fit(X_train_norm, y_train)

# Predict on training data using fitted RFC

# Evalaute RFC with test data
RFC_3_predicted = RFC_3.predict(X_test_norm)
print('Acurácia do modelo nos dados de teste: {}'.format(accuracy_score(y_test, RFC_3_predicted)))
# Create dataframe by zipping RFC feature importances and column names
rfc_features = pd.DataFrame(zip(RFC_3.feature_importances_, df.columns[:-1]), columns = ['Importância', 'Variáveis'])

# Sort in descending order for easy organization and visualization
rfc_features = rfc_features.sort_values(['Importância'], ascending=False)
# Visualize RFC feature importances
sns.barplot(x = 'Importância', y = 'Variáveis', data = rfc_features, )
plt.title('Importância individual de variáveis no diagnóstico')
sns.set_style("whitegrid")
plt.gcf().set_size_inches(30,10)
plt.show()

# remover variáveis menos revelantes

X_train.drop('fractal_dimension_se', axis=1, inplace=True)
X_train.drop('texture_worst', axis=1, inplace=True)
X_train.drop('symmetry_worst', axis=1, inplace=True)
X_train.drop('radius_worst', axis=1, inplace=True)
X_train.drop('smoothness_worst', axis=1, inplace=True)
X_train.drop('compactness_se', axis=1, inplace=True)
X_train.drop('concave_points_se', axis=1, inplace=True)
X_train.drop('perimeter_worst', axis=1, inplace=True)
X_train.drop('concavity_se', axis=1, inplace=True)
X_train.drop('perimeter_mean', axis=1, inplace=True)
X_train.drop('area_mean', axis=1, inplace=True)
X_train.drop('radius_se', axis=1, inplace=True)
X_train.drop('perimeter_se', axis=1, inplace=True)
X_train.drop('compactness_mean', axis=1, inplace=True)
X_train.drop('texture_mean', axis=1, inplace=True)
X_train.drop('texture_se', axis=1, inplace=True)
X_train.drop('fractal_dimension_worst', axis=1, inplace=True)
X_train.drop('compactness_worst', axis=1, inplace=True)
X_train.drop('smoothness_mean', axis=1, inplace=True)
X_train.drop('smoothness_se', axis=1, inplace=True)

val_features.drop('fractal_dimension_se', axis=1, inplace=True)
val_features.drop('texture_worst', axis=1, inplace=True)
val_features.drop('symmetry_worst', axis=1, inplace=True)
val_features.drop('radius_worst', axis=1, inplace=True)
val_features.drop('smoothness_worst', axis=1, inplace=True)
val_features.drop('compactness_se', axis=1, inplace=True)
val_features.drop('concave_points_se', axis=1, inplace=True)
val_features.drop('perimeter_worst', axis=1, inplace=True)
val_features.drop('concavity_se', axis=1, inplace=True)
val_features.drop('perimeter_mean', axis=1, inplace=True)
val_features.drop('area_mean', axis=1, inplace=True)
val_features.drop('radius_se', axis=1, inplace=True)
val_features.drop('perimeter_se', axis=1, inplace=True)
val_features.drop('compactness_mean', axis=1, inplace=True)
val_features.drop('texture_mean', axis=1, inplace=True)
val_features.drop('texture_se', axis=1, inplace=True)
val_features.drop('fractal_dimension_worst', axis=1, inplace=True)
val_features.drop('compactness_worst', axis=1, inplace=True)
val_features.drop('smoothness_mean', axis=1, inplace=True)
val_features.drop('smoothness_se', axis=1, inplace=True)

# construção do modelo usando keras
inputs = {}

for name, column in X_train.items():
  dtype = column.dtype
  if dtype == object:
    dtype = tf.string
  else:
    dtype = tf.float32

  inputs[name] = tf.keras.Input(shape=(1,), name=name, dtype=dtype)

inputs

# pré-processamento - normalização
numeric_inputs = {name:input for name,input in inputs.items()
                  if input.dtype==tf.float32}

x = layers.Concatenate()(list(numeric_inputs.values()))
#x = list(numeric_inputs.values())
norm = preprocessing.Normalization()
norm.adapt(np.array(df[numeric_inputs.keys()]))
all_numeric_inputs = norm(x)

all_numeric_inputs

# Coletar todos resultados de preprocessamento, para concatenar-los depois.
preprocessed_inputs = [all_numeric_inputs]

# transformação dos dados de entrada
for name, input in inputs.items():
  if input.dtype == tf.float32:
    continue
  
  lookup = preprocessing.StringLookup(vocabulary=np.unique(X_train[name]))
  one_hot = preprocessing.CategoryEncoding(max_tokens=lookup.vocab_size())

  x = lookup(input)
  x = one_hot(x)
  preprocessed_inputs.append(x)

df_preprocessing = tf.keras.Model(inputs, preprocessed_inputs)
tf.keras.utils.plot_model(model = df_preprocessing , rankdir="LR", dpi=72, show_shapes=True)

# Converter o model para um dicionário de tensors:
df_features_dict = {name: np.array(value) 
                         for name, value in X_train.items()}

# Rodar dados de amostra pelo preprocessamento para validação dos resultados
features_dict = {name:values[:1] for name, values in df_features_dict.items()}
df_preprocessing(features_dict)

# construção do modelo para predições
def df_model(preprocessing_head, inputs):
  body = tf.keras.Sequential([
    layers.Dense(128,activation='relu', kernel_regularizer=regularizers.l2(0.001)),
    layers.Dense(64,activation='relu'),
    layers.Dense(1)
  ])

  preprocessed_inputs = preprocessing_head(inputs)
  result = body(preprocessed_inputs)
  model = tf.keras.Model(inputs, result)

  model.compile(loss='mse', optimizer='adam', metrics=['mae', 'accuracy'])
  return model

df_model = df_model(df_preprocessing, inputs)

val_features_dict = {name: np.array(value) 
                         for name, value in val.items()}
history_1 = df_model.fit(x=df_features_dict, y=y_train,epochs=250,
                        validation_data=(val_features_dict, val_labels))

# Pós-treino, visualização dos resultados
# acurácia de predição:  
#lembrar: features são os inputs, labels são os targets     x = features,  y = targets
results = df_model.evaluate(df_features_dict, y_train, batch_size=1024)
print("test loss, test acc:", results)

# exibir um gráfico da perda, que é a distância entre os valores previstos e os reais durante o treino e validação
import matplotlib.pyplot as plt
# Usar a métrica de modelagem MAE
train_loss = history_1.history['mae']
val_loss = history_1.history['mae']
epochs = range(1, len(train_loss) + 1)

plt.plot(epochs, train_loss, 'g.', label='Perda em treino')
plt.plot(epochs, val_loss, 'b', label='Perda em validação')
plt.title('Perda em treino e validação')
plt.xlabel('Épocas')
plt.ylabel('Perda')
plt.legend()
plt.show()

# Excluir as primeiras épocas para tornar o gráfico mais fácil de ler
SKIP = 20

plt.plot(epochs[SKIP:], train_loss[SKIP:], 'g.', label='Perda em treino')
plt.plot(epochs[SKIP:], val_loss[SKIP:], 'b.', label='Perda em validação')
plt.title('Perda em treino e validação')
plt.xlabel('Épocas')
plt.ylabel('Perda')
plt.legend()
plt.show()

# Salvar o modelo para uso depois em forma de pacote
df_model.save('test')
reloaded = tf.keras.models.load_model('test')

!zip -r test.zip test