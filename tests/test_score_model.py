from src.score_model import ScoreModel


def test_scoring():
    model_output_path = "tests/fixtures/train_short_output.csv"
    labels_path = "tests/fixtures/train_short_labels.csv"
    scorer = ScoreModel(model_output_path, labels_path)
    assert (scorer.confusion_matrix) == {
        "true positive": 23,
        "true negative": 25,
        "false positive": 0,
        "false negative": 2,
    }
    assert (scorer.accuracy()) == 0.96
    assert (scorer.misclassification()) == 0.04
    assert (scorer.precision()) == 1.0
    assert (scorer.sensitivity()) == 0.92
    assert (scorer.specificity()) == 1.0
