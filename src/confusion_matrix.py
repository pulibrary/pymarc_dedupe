class ConfusionMatrix:
    def __init__(self, labels_data, model_data):
        self.labels_data = labels_data
        self.model_data = model_data
        self.confusion_matrix = self.build_matrix()

    def build_matrix(self):
        confusion_matrix = dict(
            [
                ("true positive", 0),
                ("true negative", 0),
                ("false positive", 0),
                ("false negative", 0),
            ]
        )
        for label_row in self.labels_data:
            first_cluster_id = self.model_data[label_row["id1"]]["Cluster ID"]
            second_cluster_id = self.model_data[label_row["id2"]]["Cluster ID"]
            label = int(label_row["label"])
            model_guess = self.model_guess(first_cluster_id, second_cluster_id)
            if label == model_guess == 1:
                confusion_matrix["true positive"] += 1
            elif label == model_guess == 0:
                confusion_matrix["true negative"] += 1
            elif label != model_guess and label == 1:
                confusion_matrix["false negative"] += 1
            elif label != model_guess and label == 0:
                confusion_matrix["false positive"] += 1
            else:
                raise ValueError(
                    "You should not be able to reach this, there is something wrong"
                )
        return confusion_matrix

    def tp(self):
        return self.confusion_matrix["true positive"]

    def tn(self):
        return self.confusion_matrix["true negative"]

    def fp(self):
        return self.confusion_matrix["false positive"]

    def fn(self):
        return self.confusion_matrix["false negative"]

    def model_guess(self, first_cluster_id, second_cluster_id):
        guess = None
        if first_cluster_id == second_cluster_id:
            guess = 1
        else:
            guess = 0
        return guess
