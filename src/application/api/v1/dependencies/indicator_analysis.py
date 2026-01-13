from typing import Annotated

from fastapi import Depends
from src.application.api.v1.controller.indicator_analysis import (
    IndicatorAnalysisController,
)
from src.application.api.v1.dependencies.common.session import VerifiedSessionDep
from src.core.domain.service.indicator_analysis import IndicatorAnalysisService
from src.core.domain.use_case.indicator_analysis import IndicatorAnalysisUseCase
from src.infrastructure.repositories.indicator_analysis import (
    IndicadorAnalysisRepositoryPostgres,
)


async def get_indicator_analysis_controller(
    session: VerifiedSessionDep,
) -> IndicatorAnalysisController:
    indicator_analysis_repository = IndicadorAnalysisRepositoryPostgres(session=session)
    indicator_analysis_service = IndicatorAnalysisService(indicator_analysis_repository)
    indicator_analysis_use_case = IndicatorAnalysisUseCase(indicator_analysis_service)
    return IndicatorAnalysisController(indicator_analysis_use_case)


IndicatorRepositoryDep = Annotated[
    IndicatorAnalysisController, Depends(get_indicator_analysis_controller)
]
