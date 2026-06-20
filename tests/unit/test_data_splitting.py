from fraud_detection.data.splitting import (
    assert_no_split_overlap,
    split_train_validation_test,
)
from tests.unit.test_data_contract import valid_data


def test_split_is_deterministic_and_has_no_overlap():
    data = valid_data()
    data = data.loc[data.index.repeat(10)].reset_index(drop=True)
    first = split_train_validation_test(data, "is_fraud", 0.2, 0.2, 42)
    second = split_train_validation_test(data, "is_fraud", 0.2, 0.2, 42)
    assert [part.index.tolist() for part in first] == [
        part.index.tolist() for part in second
    ]
    assert_no_split_overlap(*first)
