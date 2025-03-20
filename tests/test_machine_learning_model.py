import pytest
from src.machine_learning_model import MachineLearningModel


def test_inheritance():
    instance_of_child = TestChildClass("output_directory")
    with pytest.raises(NotImplementedError):
        instance_of_child.prepare_training("")


# pylint: disable=abstract-method
class TestChildClass(MachineLearningModel):
    def any_method(self):
        return True


# pylint: enable=abstract-method
