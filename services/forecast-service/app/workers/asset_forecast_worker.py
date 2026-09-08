class AssetForecastWorker:

    def __init__(self, use_case):
        self.use_case = use_case

    def run(self) -> None:
        self.use_case.process()

