from event_contracts.asset_events import AssetCreatedEvent, AssetUpdatedEvent



class AssetForecastRequirementHandler:

    def __init__(self, requirement_service):
        self.requirement_service = requirement_service

    def handle(self, event: AssetUpdatedEvent|AssetCreatedEvent):
        self.requirement_service.require(
            asset_id=event.asset_id,
            revision=event.revision,
        )