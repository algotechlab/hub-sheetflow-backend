from src.core.domain.dtos.indicator_analysis import IndicatorAnalysisBaseDto
from src.core.domain.interface.indicator_analysis import (
    IndicatorAnalysisRepositoriesInterface,
)


class IndicatorAnalysisService:
    def __init__(
        self, indicator_analysis_repository: IndicatorAnalysisRepositoriesInterface
    ):
        self.indicator_analysis_repository = indicator_analysis_repository

    async def get_summary_indicator_analysis(self) -> IndicatorAnalysisBaseDto | None:
        return await self.indicator_analysis_repository.get_summary_indicator_analysis()
