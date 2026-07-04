import pandas as pd

from src.structure import add_confirmed_structure, classify_structure_regime


def sample_structure_data():
    dates = pd.date_range("2024-01-01", periods=8, freq="D")

    return pd.DataFrame({
        "Open":  [10, 11, 12, 11, 10, 12, 14, 15],
        "High":  [11, 12, 13, 12, 11, 13, 15, 16],
        "Low":   [9, 10, 11, 10, 9, 11, 13, 14],
        "Close": [10, 11, 12, 10, 9, 13, 15, 16],
        "Volume": [100] * 8,
    }, index=dates)


def test_add_confirmed_structure_creates_columns():
    df = sample_structure_data()
    result = add_confirmed_structure(df)

    assert "Bull Break" in result.columns
    assert "Bear Break" in result.columns
    assert "Bull Count" in result.columns
    assert "Bear Count" in result.columns


def test_classify_structure_regime_creates_regime_column():
    df = sample_structure_data()
    structure = add_confirmed_structure(df)
    result = classify_structure_regime(structure)

    assert "Structure Regime" in result.columns
    assert len(result) == len(df)