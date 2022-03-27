from typing import Dict

from xsdata.formats.dataclass.filters import Filters
from xsdata.formats.dataclass.generator import DataclassGenerator
from xsdata.models.config import GeneratorConfig
from xsdata.utils.text import stop_words

stop_words.update(("schema", "validate"))


class PydanticGenerator(DataclassGenerator):
    """Python pydantic dataclasses code generator."""

    @classmethod
    def init_filters(cls, config: GeneratorConfig) -> Filters:
        return PydanticFilters(config)


class PydanticFilters(Filters):
    @classmethod
    def build_import_patterns(cls) -> Dict[str, Dict]:
        patterns = super().build_import_patterns()
        type_patterns = cls.build_type_patterns
        patterns.update(
            {
                "dataclasses": {"field": [" = field("]},
                "pydantic.dataclasses": {"dataclass": ["@dataclass"]},
                "xsdata.models.datatype": {},
                "xsdata_pydantic.datatype": {
                    "XmlDate": type_patterns("XmlDate"),
                    "XmlDateTime": type_patterns("XmlDateTime"),
                    "XmlDuration": type_patterns("XmlDuration"),
                    "XmlPeriod": type_patterns("XmlPeriod"),
                    "XmlTime": type_patterns("XmlTime"),
                },
            }
        )

        return {key: patterns[key] for key in sorted(patterns)}
