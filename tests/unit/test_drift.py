from fraud_detection.monitoring.drift import classify_psi, population_stability_index


def test_psi_detects_stable_distribution():
    expected = [float(value) for value in range(100)]
    actual = [float(value) for value in range(100)]
    psi = population_stability_index(expected, actual)
    assert psi < 0.01
    assert classify_psi(psi) == "stable"


def test_psi_detects_drift():
    expected = [float(value) for value in range(100)]
    actual = [float(value + 100) for value in range(100)]
    psi = population_stability_index(expected, actual)
    assert classify_psi(psi) == "significant_drift"
