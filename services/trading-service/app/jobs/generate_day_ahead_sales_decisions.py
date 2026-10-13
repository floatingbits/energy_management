"""Generate day-ahead sales decisions for all known portfolios.

    docker compose run --rm --user=1000:1000 trading-service \
        python -m app.jobs.generate_day_ahead_sales_decisions
"""

from app.decisions.bootstrap import (
    create_day_ahead_sales_decision_service,
    create_portfolio_client,
)


class GenerateDayAheadSalesDecisionJob:
    """One portfolio's decision."""

    def __init__(self, service):
        self.service = service

    def run(self, portfolio_id: int):
        return self.service.decide_for_portfolio(portfolio_id)


class GenerateAllDayAheadSalesDecisionsJob:

    def __init__(self, portfolio_client, service):
        self.portfolio_client = portfolio_client
        self.service = service

    def run(self):
        portfolios = self.portfolio_client.get_portfolios()

        failures = []
        job = GenerateDayAheadSalesDecisionJob(self.service)
        for portfolio in portfolios:
            try:
                result = job.run(portfolio["id"])
            except Exception as error:  # noqa: BLE001 (per-portfolio isolation)
                failures.append((portfolio["id"], error))
        if failures:
            details = "; ".join(f"{pid}: {error}" for pid, error in failures)
            raise RuntimeError(
                f"Day-ahead decisions failed for some portfolios: {details}"
            )
        return len(portfolios)


def main():
    service = create_day_ahead_sales_decision_service()
    client = create_portfolio_client()

    job = GenerateAllDayAheadSalesDecisionsJob(client, service)
    job.run()


if __name__ == "__main__":
    main()
