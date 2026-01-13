from src.core.domain.dtos.indicator_analysis import IndicatorAnalysisBaseDto
from src.core.domain.service.indicator_analysis import IndicatorAnalysisService


class IndicatorAnalysisUseCase:
    def __init__(self, indicator_analysis_service: IndicatorAnalysisService):
        self.indicator_analysis_service = indicator_analysis_service

    async def get_summary_indicator_analysis(self) -> IndicatorAnalysisBaseDto:
        return await self.indicator_analysis_service.get_summary_indicator_analysis()
