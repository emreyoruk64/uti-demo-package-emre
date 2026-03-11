
from sdks.novavision.src.helper.package import PackageHelper
from components.DemoPackageEmre.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, PackageExecutor1Outputs, PackageExecutor1Response, PackageExecutor1, OutputImage


def build_response(context):
    outputImage = OutputImage(value=context.image)
    packageExecutor1Outputs = PackageExecutor1Outputs(outputImage=outputImage)
    packageExecutor1Response = PackageExecutor1Response(outputs=packageExecutor1Outputs)
    packageExecutor1 = PackageExecutor1(value=packageExecutor1Response)
    executor = ConfigExecutor(value=packageExecutor1)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel