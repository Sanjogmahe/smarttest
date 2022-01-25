import evalml
import pandas as pd

df = pd.read_excel('SampleTestData.xlsx', index_col=0)
df.drop(columns="Release ID",inplace=True)
print(df.columns)

r = pd.concat([df,df,df])

X=r.drop(columns = 'Test Case Title ')#,axis=1)
y=r['Test Case Title ']

X_train = X

y_train = y

automl = evalml.automl.AutoMLSearch(X_train=X, y_train=y, data_split=None, problem_type='multiclass',verbose=True)
automl.search()

from evalml.model_understanding.graphs import confusion_matrix
import pickle


best_pipeline = automl.best_pipeline
automl.describe_pipeline(automl.rankings.iloc[0]["id"])

# scores = best_pipeline.score(X_holdout, y_holdout,  objectives=evalml.objectives.get_core_objectives('multiclass'))
scores = best_pipeline.score(X_train, y_train,  objectives=evalml.objectives.get_core_objectives('multiclass'))


print(f'Accuracy Binary: {scores["Accuracy Multiclass"]}')

y_pred = best_pipeline.predict(X_train)
print('Prdiction is',y_pred)
mat=confusion_matrix(y_train, y_pred)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
print('\nAccuracy: {:.2f}\n'.format(accuracy_score(y_train, y_pred)))



with open("pipeline.pkl", 'wb') as f:
    pickle.dump(best_pipeline, f)

print(automl.rankings)

output = pd.DataFrame(y_pred)
output.to_csv('notebooks/output.csv')
output_read = pd.read_csv('notebooks/output.csv')


# test cases run
from datetime import date
from common_function import url, iframe, justCli, hover, clear, justEnt, quit, default_iframe, CancelAlert

for i in output_read['Test Case Title ']:

    today = date.today()
    d1 = today.strftime("%m/%d/%Y")

    url("https://www.google.com/")

    quit()