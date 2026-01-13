from fastapi import APIRouter, status
from src.application.api.v1.dependencies.indicator_analysis import (
    IndicatorRepositoryDep,
)
from src.application.api.v1.schemas.indicator_analysis import (
    IndicatorAnalysisBaseSchema,
)

tags_metadata = {
    'name': 'Indicadores',
    'description': ('Modulo de indicadores.'),
}

router = APIRouter(
    prefix='/indicator-analysis',
    tags=[tags_metadata['name']],
)


@router.get(
    '',
    description='Rota para listar os indicadores',
    status_code=status.HTTP_200_OK,
    response_model=IndicatorAnalysisBaseSchema,
)
async def get_summary_indicator_analysis(
    controller: IndicatorRepositoryDep,
) -> IndicatorAnalysisBaseSchema:
    return await controller.get_summary_indicator_analysis()
