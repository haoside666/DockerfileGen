from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
import os
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature


class FeatureInfoGeneratorYum(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        if not self.does_first_operand_equal_arg("clean"):
            if self.does_first_operand_equal_arg("install") and self.get_operand_list_length() == 2:
                operand_list = self.cmd_inv_after_io.operand_list
                package_name: str = operand_list[1].get_name()
                if package_name.endswith(".rpm"):
                    pkg_name = extract_tar_filename(package_name)
                    self.add_one_element_to_operand_list(pkg_name, (WhichClassForFeature.PKG, None))
                else:
                    self.all_but_first_operand_is_pkg()
            else:
                self.all_but_first_operand_is_pkg()


def extract_tar_filename(archive_name: str):
    archive_name = os.path.basename(archive_name)
    index = archive_name.find(".rpm")
    if index != -1:
        return archive_name[:index]
