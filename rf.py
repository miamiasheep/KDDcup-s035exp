from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

def RFC(train, valid, features, param):
	model = RandomForestClassifier(**param)
	model.fit(train[features], train["ans"])
	
	train_predict = model.predict_proba(train[features])[:,1]
	valid_predict = model.predict_proba(valid[features])[:,1]
	
	train_auc = roc_auc_score(train["ans"].values, train_predict)
	valid_auc = -1.
	if "ans" in valid.columns:
		valid_auc = roc_auc_score(valid["ans"].values, valid_predict)
	ret = dict()
	ret['train_auc'] = train_auc
	ret['valid_auc'] = valid_auc
	ret['train_predict'] = train_predict
	ret['valid_predict'] = valid_predict
	ret['importance'] = model.feature_importances_
	return ret
