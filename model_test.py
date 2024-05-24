import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import svm, tree, linear_model, neighbors, naive_bayes, ensemble, discriminant_analysis, gaussian_process

# 加载数据集
data = pd.read_csv('..\\dataset\\new_merged.csv',encoding = 'gbk')

# 假设最后一列是目标变量
X = data.iloc[:, :4]

from sklearn.preprocessing import LabelEncoder

# 对所有的分类变量进行标签编码
for col in X.columns:
    if X[col].dtype == 'object':
        lbl = LabelEncoder()
        lbl.fit(list(X[col].values))
        X[col] = lbl.transform(list(X[col].values))

X = X.fillna(X.mean())
y = data.iloc[:, 4]

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 定义模型
from sklearn.model_selection import GridSearchCV

# 定义模型和对应的参数网格
models_and_params = {
    'AdaBoostClassifier': {
        'model': ensemble.AdaBoostClassifier(),
        'params': {
            'n_estimators': [50, 100, 150],
            'learning_rate': [0.01, 0.1, 1]
        }
    },
    'BaggingClassifier': {
        'model': ensemble.BaggingClassifier(),
        'params': {
            'n_estimators': [10, 20, 30],
            'max_samples': [0.5, 1.0],
            'max_features': [0.5, 1.0]
        }
    },
    'ExtraTreesClassifier': {
        'model': ensemble.ExtraTreesClassifier(),
        'params': {
            'n_estimators': [50, 100, 150],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'bootstrap': [True, False]
        }
    },
    'GradientBoostingClassifier': {
        'model': ensemble.GradientBoostingClassifier(),
        'params': {
            'learning_rate': [0.01, 0.1, 0.2],
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 4, 5],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'subsample': [0.5, 0.8, 1.0]
        }
    },
    'RandomForestClassifier': {
        'model': ensemble.RandomForestClassifier(),
        'params': {
            'n_estimators': [100, 200, 300],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'bootstrap': [True, False]
        }
    },
    'GaussianProcessClassifier': {
        'model': gaussian_process.GaussianProcessClassifier(),
        'params': {
            'max_iter_predict': [100, 200, 300],
            'n_restarts_optimizer': [0, 1, 2],
            'warm_start': [True, False],
            'copy_X_train': [True, False]
        }
    },
    'LogisticRegressionCV': {
        'model': linear_model.LogisticRegressionCV(),
        'params': {
            'Cs': [1, 10, 100],
            'fit_intercept': [True, False],
            'cv': [3, 5, 10],
            'dual': [False, True],
            'penalty': ['l1', 'l2'],
            'scoring': ['accuracy'],
            'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'],
            'tol': [0.0001, 0.001, 0.01, 0.1],
            'max_iter': [100, 200, 300]
        }
    },
    'PassiveAggressiveClassifier': {
        'model': linear_model.PassiveAggressiveClassifier(),
        'params': {
            'C': [0.1, 1.0, 10.0],
            'fit_intercept': [True, False],
            'max_iter': [1000, 2000, 3000],
            'tol': [0.001, 0.01, 0.1],
            'early_stopping': [True, False],
            'validation_fraction': [0.1, 0.2, 0.3],
            'n_iter_no_change': [5, 10, 15],
            'shuffle': [True, False],
            'loss': ['hinge', 'squared_hinge'],
            'n_jobs': [-1]
        }
    },
    'RidgeClassifierCV': {
        'model': linear_model.RidgeClassifierCV(),
        'params': {
            'alphas': [(0.1, 1.0, 10.0)],
            'fit_intercept': [True, False],
            'normalize': [True, False],
            'scoring': ['accuracy'],
            'cv': [None, 2, 3, 4, 5],
            'class_weight': [None, 'balanced']
        }
    },
    'SGDClassifier': {
        'model': linear_model.SGDClassifier(),
        'params': {
            'loss': ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron'],
            'penalty': ['l2', 'l1', 'elasticnet'],
            'alpha': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
            'l1_ratio': [0.15, 0.3, 0.5, 0.7, 1],
            'fit_intercept': [True, False],
            'max_iter': [1000, 2000, 3000],
            'tol': [0.001, 0.01, 0.1],
            'shuffle': [True, False],
            'verbose': [0, 1, 2, 3],
            'epsilon': [0.1, 0.01, 0.001, 0.0001],
            'n_jobs': [-1],
            'random_state': [None, 42],
            'learning_rate': ['optimal', 'constant', 'invscaling', 'adaptive'],
            'eta0': [0.01, 0.1, 1, 10, 100]
        }
    },
    'Perceptron': {
        'model': linear_model.Perceptron(),
        'params': {
            'penalty': [None, 'l2', 'l1', 'elasticnet'],
            'alpha': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100],
            'fit_intercept': [True, False],
            'max_iter': [1000, 2000, 3000],
            'tol': [0.001, 0.01, 0.1],
            'shuffle': [True, False],
            'verbose': [0, 1, 2, 3],
            'eta0': [1.0, 10.0, 100.0],
            'n_jobs': [-1],
            'random_state': [None, 42],
            'early_stopping': [False, True],
            'validation_fraction': [0.1, 0.2, 0.3],
            'n_iter_no_change': [5, 10, 15],
            'class_weight': [None, 'balanced'],
            'warm_start': [False, True]
        }
    },
    'BernoulliNB': {
        'model': naive_bayes.BernoulliNB(),
        'params': {
            'alpha': [0.1, 1.0, 10.0],
            'binarize': [0.0, 0.5, 1.0],
            'fit_prior': [True, False],
            'class_prior': [None, [0.5, 0.5]]
        }
    },
    'GaussianNB': {
        'model': naive_bayes.GaussianNB(),
        'params': {
            'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]
        }
    },
    'KNeighborsClassifier': {
        'model': neighbors.KNeighborsClassifier(),
        'params': {
            'n_neighbors': [3, 5, 7, 9, 11],
            'weights': ['uniform', 'distance'],
            'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
            'leaf_size': [10, 20, 30, 40, 50],
            'p': [1, 2]
        }
    },
    'SVC': {
        'model': svm.SVC(),
        'params': {
            'C': [0.1, 1, 10, 100, 1000],
            'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'degree': [0, 1, 2, 3, 4, 5, 6]
        }
    },
    'NuSVC': {
        'model': svm.NuSVC(),
        'params': {
            'nu': [0.1, 0.5, 0.7],
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'degree': [0, 1, 2, 3, 4, 5, 6],
            'gamma': ['scale', 'auto']
        }
    },
    'LinearSVC': {
        'model': svm.LinearSVC(),
        'params': {
            'penalty': ['l1', 'l2'],
            'loss': ['hinge', 'squared_hinge'],
            'dual': [True, False],
            'tol': [0.0001, 0.001, 0.01, 0.1],
            'C': [0.1, 1, 10, 100, 1000],
            'multi_class': ['ovr', 'crammer_singer'],
            'fit_intercept': [True, False],
            'intercept_scaling': [1, 2, 3, 4, 5],
            'class_weight': [None, 'balanced'],
            'verbose': [0, 1, 2, 3],
            'random_state': [None, 42],
            'max_iter': [1000, 2000, 3000]
        }
    },
    'DecisionTreeClassifier': {
        'model': tree.DecisionTreeClassifier(),
        'params': {
            'criterion': ['gini', 'entropy'],
            'splitter': ['best', 'random'],
            'max_depth': [None, 10, 20, 30, 40, 50],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'min_weight_fraction_leaf': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            'max_features': [None, 'auto', 'sqrt', 'log2'],
            'random_state': [None, 42],
            'max_leaf_nodes': [None, 10, 20, 30, 40, 50],
            'min_impurity_decrease': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            'class_weight': [None, 'balanced']
        }
    },
    'ExtraTreeClassifier': {
        'model': tree.ExtraTreeClassifier(),
        'params': {
            'criterion': ['gini', 'entropy'],
            'splitter': ['random'],
            'max_depth': [None, 10, 20, 30, 40, 50],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'min_weight_fraction_leaf': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            'max_features': ['auto', 'sqrt', 'log2'],
            'random_state': [None, 42],
            'max_leaf_nodes': [None, 10, 20, 30, 40, 50],
            'min_impurity_decrease': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            'class_weight': [None, 'balanced']
        }
    },
    'LinearDiscriminantAnalysis': {
        'model': discriminant_analysis.LinearDiscriminantAnalysis(),
        'params': {
            'solver': ['svd', 'lsqr', 'eigen'],
            'shrinkage': [None, 'auto', 0.1, 0.5, 0.9],
            'n_components': [None, 1, 2, 3, 4, 5],
            'store_covariance': [False, True],
            'tol': [0.0001, 0.001, 0.01, 0.1]
        }
    },
    'QuadraticDiscriminantAnalysis': {
        'model': discriminant_analysis.QuadraticDiscriminantAnalysis(),
        'params': {
            'reg_param': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            'store_covariance': [False, True],
            'tol': [0.0001, 0.001, 0.01, 0.1]
        }
    },
}

# 对每个模型进行网格搜索
for name, mp in models_and_params.items():
    start_time = time.time()
    grid = GridSearchCV(mp['model'], mp['params'], cv=5)
    grid.fit(X_train, y_train)
    end_time = time.time()
    print(f"Model: {name}, Best parameters: {grid.best_params_}, Best score: {grid.best_score_}, Training time: {end_time - start_time}s")