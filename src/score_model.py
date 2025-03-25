import csv
from src.confusion_matrix import ConfusionMatrix


class ScoreModel:
    def __init__(self, model_csv, labels_csv):
        self.model_data = self.read_model_data(model_csv)
        self.labels_data = self.read_labels_data(labels_csv)
        matrix_obj = ConfusionMatrix(self.labels_data, self.model_data)
        self.confusion_matrix = ConfusionMatrix(
            self.labels_data, self.model_data
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
                # data_d[row["id"]] = dict([("cluster_id", row["Cluster ID"])])
                data_d[row["id"]] = dict(row)
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

    # Same as recall
    def sensitivity(self):
        return (self.tp) / (self.tp + self.fn)

    def specificity(self):
        return (self.tn) / (self.tn + self.fp)

    def write_false_negatives_to_file(self):
        output_file = 'experiments_files_and_output/false_negatives.csv'
        with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.model_data.get('id.6d631bb460').keys())
            writer.writeheader()
            for label_row in self.labels_data:
                first_model_row = self.model_data[label_row["id1"]]
                second_model_row = self.model_data[label_row["id2"]]
                first_cluster_id = first_model_row["Cluster ID"]
                second_cluster_id = second_model_row["Cluster ID"]
                label = int(label_row["label"])
                model_guess = self.model_guess(first_cluster_id, second_cluster_id)
                if label != model_guess and label == 1:
                    writer.writerow(first_model_row)
                    writer.writerow(second_model_row)


    def model_guess(self, first_cluster_id, second_cluster_id):
        guess = None
        if first_cluster_id == second_cluster_id:
            guess = 1
        else:
            guess = 0
        return guess