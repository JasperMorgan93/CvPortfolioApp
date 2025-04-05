from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self) -> List[Dict[str, Any]]:
        pass
    