from tools.box_validator import BoxValidator
# TODO: Import from new location after refactor


class TestValidationUtils:
    def test_can_validate_size(self):
        validator = BoxValidator()
        assert validator.size_validation([[0, 0], [1, 1]]) is True
