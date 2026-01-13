from abc import ABC, abstractmethod

from src.core.domain.dtos.indicator_analysis import IndicatorAnalysisBaseDto


class IndicatorAnalysisRepositoriesInterface(ABC):
    @abstractmethod
    async def get_summary_indicator_analysis(self) -> IndicatorAnalysisBaseDto: ...

    @abstractmethod
    async def get_overview_indicator_analysis(self): ...
