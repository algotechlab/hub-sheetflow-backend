from src.application.api.v1.schemas.indicator_analysis import (
    IndicatorAnalysisBaseSchema,
)
from src.core.domain.use_case.indicator_analysis import IndicatorAnalysisUseCase


class IndicatorAnalysisController:
    def __init__(self, use_case: IndicatorAnalysisUseCase):
        self.use_case = use_case

    async def get_summary_indicator_analysis(self) -> IndicatorAnalysisBaseSchema:
        indicator_analysis = await self.use_case.get_summary_indicator_analysis()
        return IndicatorAnalysisBaseSchema.model_validate(
            indicator_analysis.model_dump()
        )
