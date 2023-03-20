import json
from dataclasses import dataclass
from typing import Any, List


@dataclass
class KernelSetting:
    name: str
    filterType: str
    blurOrSharpenCheckbox: bool
    kernelSize: str
    sigma: str
    sigma2: str
    timeFiltersApllied: str

    @staticmethod
    def from_dict(obj: Any) -> "KernelSetting":
        _name = str(obj.get("name"))
        _filterType = str(obj.get("filterType"))
        _blurOrSharpenCheckbox = bool(obj.get("blurOrSharpenCheckbox"))
        _kernelSize = str(obj.get("kernelSize"))
        _sigma = str(obj.get("sigma"))
        _sigma2 = str(obj.get("sigma2"))
        _timeFiltersApllied = str(obj.get("timeFiltersApllied"))
        return KernelSetting(
            _name,
            _filterType,
            _blurOrSharpenCheckbox,
            _kernelSize,
            _sigma,
            _sigma2,
            _timeFiltersApllied,
        )


@dataclass
class FilterSettings:
    settings: List[KernelSetting]

    @staticmethod
    def from_dict(obj: Any) -> "FilterSettings":
        _settings = [KernelSetting.from_dict(y) for y in obj.get("settings")]
        return FilterSettings(_settings)

    @staticmethod
    def import_config(file_path: str) -> "FilterSettings":
        with open(file_path, "r") as file:
            json_string = file.read()

        # Parse the JSON string into a Python dictionary
        json_data = json.loads(json_string)
        return FilterSettings.from_dict(json_data)


filter_settings = FilterSettings.import_config(
    file_path=r"C:\Users\voli\Desktop\config.txt"
)
print(filter_settings.settings)
