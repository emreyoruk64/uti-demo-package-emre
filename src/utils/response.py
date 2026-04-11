
from sdks.novavision.src.helper.package import PackageHelper
from components.DemoPackageEmre.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, PackageExecutor1Outputs, PackageExecutor2Outputs, PackageExecutor1Response, PackageExecutor2Response, PackageExecutor1, PackageExecutor2, OutputImage, OutputImageTwo


def build_response_gray(context):
    outputImage = OutputImage(value=context.image)
    packageExecutor1Outputs = PackageExecutor1Outputs(outputImage=outputImage)
    packageExecutor1Response = PackageExecutor1Response(outputs=packageExecutor1Outputs)
    packageExecutor1 = PackageExecutor1(value=packageExecutor1Response)
    executor = ConfigExecutor(value=packageExecutor1)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_response_mix(context):
    outputImage = OutputImage(value=context.image)
    outputImageTwo = OutputImageTwo(value=context.image_two)
    packageExecutor2Outputs = PackageExecutor2Outputs(outputImage=outputImage, outputImageTwo=outputImageTwo)
    packageExecutor2Response = PackageExecutor2Response(outputs=packageExecutor2Outputs)
    packageExecutor2 = PackageExecutor2(value=packageExecutor2Response)
    executor = ConfigExecutor(value=packageExecutor2)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
