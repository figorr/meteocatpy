def test_imports():
    from meteocatpy import (
        MeteocatTown,
        MeteocatForecast,
        MeteocatSymbols,
        MeteocatStations,
        MeteocatTownStations,
        MeteocatStationData,
        MeteocatVariables,
    )

    assert MeteocatTown is not None
    assert MeteocatForecast is not None
    assert MeteocatSymbols is not None
    assert MeteocatStations is not None
    assert MeteocatTownStations is not None
    assert MeteocatStationData is not None
    assert MeteocatVariables is not None
