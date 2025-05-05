import pytest
from src.machine_learning_model import MachineLearningModel


def test_inheritance():
    instance_of_child = TestChildClass("output_directory")
    with pytest.raises(NotImplementedError):
        instance_of_child.prepare_training("")


# pylint: disable=abstract-method
# pylint: disable=useless-parent-delegation
class TestChildClass(MachineLearningModel):
    def __init__(self, output_directory, match_threshold=0.5):
        super().__init__(output_directory, match_threshold)


# pylint: enable=abstract-method
# pylint: enable=useless-parent-delegation
