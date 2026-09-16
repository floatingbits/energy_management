import argparse

from app.bootstrap.workers import (
    create_portfolio_forecast_updater,
)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Aggregates persisted asset forecasts into "
            "portfolio forecasts."
        )
    )

    parser.add_argument(
        "--portfolio-id",
        type=int,
        default=None,
        help=(
            "Aggregiert nur dieses Portfolio; ohne Angabe "
            "alle Portfolios."
        )
    )

    args = parser.parse_args()

    updater = create_portfolio_forecast_updater(
        portfolio_id=args.portfolio_id
    )

    updater.run()


if __name__ == "__main__":
    main()
