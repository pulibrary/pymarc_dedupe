import csv
from src.confusion_matrix import ConfusionMatrix


class ScoreModel:
    def __init__(self, model_csv, labels_csv):
        model_data = self.read_model_data(model_csv)
        labels_data = self.read_labels_data(labels_csv)
        matrix_obj = ConfusionMatrix(labels_data, model_data)
        self.confusion_matrix = ConfusionMatrix(
            labels_data, model_data
        ).confusion_matrix
        self.tp = matrix_obj.tp()
        self.tn = matrix_obj.tn()
        self.fp = matrix_obj.fp()
        self.fn = matrix_obj.fn()

    def read_model_data(self, model_csv):
        data_d = {}
        with open(model_csv, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_d[row["id"]] = dict([("cluster_id", row["Cluster ID"])])
        return data_d

    def read_labels_data(self, labels_csv):
        data_l = []
        with open(labels_csv, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_l.append(row)
        return data_l

    def accuracy(self):
        return (self.tp + self.tn) / (self.tp + self.tn + self.fp + self.fn)

    def misclassification(self):
        return (self.fp + self.fn) / (self.tp + self.tn + self.fp + self.fn)

    def precision(self):
        return (self.tp) / (self.tp + self.fp)

    def sensitivity(self):
        return (self.tp) / (self.tp + self.fn)

    def specificity(self):
        return (self.tn) / (self.tn + self.fp)
