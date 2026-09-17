from app.portfolio_forecast.aggregators.naive import (
    NaivePortfolioAggregator,
)
from app.portfolio_forecast.domain.timeslice import (
    TimesliceValues,
)


def test_naive_aggregator_sums_quantiles():

    aggregator = NaivePortfolioAggregator()

    aggregated = aggregator.aggregate(
        [
            TimesliceValues(
                asset_id=1,
                quantiles={5: 1.0, 50: 2.0, 95: 3.0},
            ),
            TimesliceValues(
                asset_id=2,
                quantiles={5: 10.0, 50: 20.0, 95: 30.0},
            ),
        ]
    )

    assert aggregated.quantiles[5] == 11.0
    assert aggregated.quantiles[50] == 22.0
    assert aggregated.quantiles[95] == 33.0


def test_naive_aggregator_rejects_empty_timeslice():

    aggregator = NaivePortfolioAggregator()

    try:
        aggregator.aggregate([])
        assert False, "expected ValueError"

    except ValueError:
        pass


def test_naive_aggregator_name():

    assert NaivePortfolioAggregator().get_name() == "naive"
