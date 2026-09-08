from event_contracts.asset_events import AssetCreatedEvent, AssetUpdatedEvent


class AssetCreatedHandler:

    def __init__(self, asset_forecast_service):
        self.asset_forecast_service = asset_forecast_service

    def handle(self, event: AssetCreatedEvent):
        self.asset_forecast_service.generate(
            event.asset_id
        )




class AssetUpdatedHandler:

    def __init__(self, requirement_service):
        self.requirement_service = requirement_service

    def handle(self, event: AssetUpdatedEvent):
        self.requirement_service.require(
            asset_id=event.asset_id,
            revision=event.revision,
        )