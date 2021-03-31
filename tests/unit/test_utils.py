from common.utils.box_validator_utils import BoxValidator


# TODO: Added tests for utils

class TestsUtils:
    def test_can_validate_size(self):
        validator = BoxValidator()
        assert validator.size_validation([[0, 0], [1, 1]]) is True
