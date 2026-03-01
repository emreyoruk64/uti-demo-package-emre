
from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Detection, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class InputDetection(Input):
    name: Literal["inputDetection"] = "inputDetection"
    value: Union[List[Detection], Detection]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Detection"

class OutputDetection(Input):
    name: Literal["outputDetection"] = "outputDetection"
    value: Union[List[Detection], Detection]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Detection"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class KeepSideFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class KeepSideTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class Example1(Config):
    name: Literal["Example1"] = "Example1"
    value: float
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Example1"

class ConfigParam1(Config):
    name: Literal["ConfigParam1"] = "ConfigParam1"
    example: Example1
    value: Literal["ConfigParam1"] = "ConfigParam1"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title="Param1"


class ConfigParam2(Config):
    name: Literal["ConfigParam2"] = "ConfigParam2"
    value: Union[KeepSideTrue, KeepSideFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Param2"

class ConfigParams(Config):
     name: Literal["ConfigParams"] = "ConfigParams"
     value:Union[ConfigParam1,ConfigParam2]
     type: Literal["object"] = "object"
     field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

     class Config:
         title = "Params"

class ExecutorConfigs(Configs):
     configParams: ConfigParams

class KeepSideBBox(Config):
    """
        Rotate image without catting off sides.
    """
    name: Literal["KeepSide"] = "KeepSide"
    value: Union[KeepSideTrue, KeepSideFalse]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Keep Sides"


class Degree(Config):
    """
        Positive angles specify counterclockwise rotation while negative angles indicate clockwise rotation.
    """
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359.0, le=359.0,default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Angle"


class PackageExecutor1Inputs(Inputs):
    inputImage: InputImage


class PackageExecutor1Configs(Configs):
    degree: Degree
    drawBBox: KeepSideBBox

class PackageExecutor2Inputs(Inputs):
    inputImage: InputImage
    inputDetection: InputDetection


class PackageExecutor2Configs(Configs):
    degree: Degree
    drawBBox: KeepSideBBox


class PackageExecutor1Outputs(Outputs):
    outputImage: OutputImage

class PackageExecutor2Outputs(Outputs):
    outputImage: OutputImage
    outputDetection: OutputDetection

class PackageExecutor1Request(Request):
    inputs: Optional[PackageExecutor1Inputs]
    configs: PackageExecutor1Configs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class PackageExecutor2Request(Request):
    inputs: Optional[PackageExecutor2Inputs]
    configs: PackageExecutor2Configs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class PackageExecutor1Response(Response):
    outputs: PackageExecutor1Outputs

class PackageExecutor2Response(Response):
    outputs: PackageExecutor2Outputs

class PackageExecutor2(Config):
    name: Literal["PackageExecutor2"] = "PackageExecutor2"
    value: Union[PackageExecutor2Request, PackageExecutor2Response]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Package"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class PackageExecutor1(Config):
    name: Literal["PackageExecutor1"] = "PackageExecutor1"
    value: Union[PackageExecutor1Request, PackageExecutor1Response]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Package"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[PackageExecutor1, PackageExecutor2]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoPackageEmre"] = "DemoPackageEmre"
