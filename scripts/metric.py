#coding=utf-8
# 常用的指标计算

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# prepare y_true, y_pred list
# 分类任务的 准召，混淆矩阵
print(classification_report(y_true, y_pred))
print(confusion_matrix(y_true, y_pred))



