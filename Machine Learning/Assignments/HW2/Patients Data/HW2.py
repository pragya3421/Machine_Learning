import numpy as np
import pandas as pd
import scipy.stats as stats
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression, Lasso, LassoCV
from sklearn.model_selection import train_test_split

df=pd.read_csv('ML_HW_Data_Patients.csv')
df.info


df['Height']=stats.zscore(df['Height'])
df['Weight']=stats.zscore(df['Weight'])
df=df.drop(['Diastolic','LastName'], axis=1)
df

df['Age']=stats.zscore(df['Age'])
Gender_dummy=pd.get_dummies(df.Gender)
Smoker_dummy=pd.get_dummies(df.Smoker)
Location_dummy=pd.get_dummies(df.Location)
Self_dummy=pd.get_dummies(df.SelfAssessedHealthStatus)

new_df=pd.concat([df,Gender_dummy,Smoker_dummy,Location_dummy,Self_dummy],axis=1)
new_df.drop(labels=['Gender','Smoker','Location',"'Female'",0,'SelfAssessedHealthStatus',
                    "'St. Mary's Medical Center'","'Poor'"],axis=1,inplace=True)
new_df.rename(columns={1:'Smoker',"'Male'":'Male',"'county General Hospital'":'countyGenralHospital', "'VA Hospital'":'VAHospital',"'Excellent'":'Excellent',
                       "'Fair'":'Fair',"'Good'":'Good'},inplace=True)


X= new_df.drop(['Systolic'],axis=1)
Y=new_df['Systolic']

X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=0.033,random_state=42)
reg=LinearRegression()
reg.fit(X_train,y_train)
y_predict=reg.predict(X_test)

model=LassoCV(eps=1e-3,cv=10)
model.fit(X,Y)
alphas=model.alphas_
alpha=model.alpha_
mse_path=model.mse_path_


print('alpha:',model.alpha_)
print('Intercept:',model.intercept_)
print('Coefficients:',model.coef_)


coefs=[]
for a in alphas:
    clf=Lasso(alpha=a)
    clf.fit(X,Y)
    coefs.append(clf.coef_)
coefs_path=np.mat(coefs)


import matplotlib.pyplot as plt
import numpy as np

# Assuming `model` and `coefs_path` are already defined...

# Get a colormap
colors = plt.cm.viridis(np.linspace(0, 1, len(coefs_path)))

plt.figure(figsize=(10, 6))  # Increase the figure size for better visualization

# Plot each coefficient path with different colors
for idx, coef_path in enumerate(coefs_path):
    plt.plot(-np.log10(model.alphas_), coef_path, linestyle='-', color=colors[idx], linewidth=1.5)

ymin, ymax = plt.ylim()

# Highlight the selected alpha with a different line style and width
plt.vlines(-np.log10(model.alpha_), ymin, ymax, linestyle='dashed', linewidth=2, color='red', label='Selected alpha')

# Aesthetically appealing changes
plt.legend(loc='upper right', fontsize='small')
plt.xlabel('-log(alpha)', fontsize=14)
plt.ylabel('Regression Coefficients', fontsize=14)
plt.title('Lasso Coefficient Paths', fontsize=16)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()

plt.show()


plt.plot(-np.log10(model.alphas_),mse_path, ':')
plt.plot(-np.log10(model.alphas_),mse_path.mean(axis=-1),10)
ymin,ymax=0,60
plt.vlines(-np.log10(model.alpha_),ymin,ymax,linestyle='dotted',label='Selected alpha')
plt.legend()
plt.xlabel('-log(alpha)')
plt.ylabel('Mean square error')
plt.title('mean Square Errors on each CV fold')
plt.ylim(ymin,ymax)
plt.show()

la={}
la_df=pd.DataFrame(la)
i=0
for a in alphas:
    choose=Lasso(alpha=a)
    choose.fit(X,Y)
    la[i]=[a,choose.coef_,choose.intercept_]
    i+=1
print('\n',la)


print('Coffients:',Lasso(alpha=0.9021926169511577).fit(X,Y).coef_)