from dockdepend.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from dockdepend.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_io


class FeatureInfoGeneratorApk(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        if self.get_operand_list_length() > 0:
            if not self.does_first_operand_equal_arg("clean"):
                if self.does_first_operand_equal_arg("update"):
                    self.add_one_element_to_operand_list("apk", (WhichClassForFeature.PKG, None))
                    self.add_one_element_to_operand_list("/etc", (WhichClassForFeature.FILESTD, make_other_io()))
                else:
                    self.all_but_first_operand_is_pkg()
                    if self.cmd_inv_after_io.does_operand_list_contain(["python-", "python3-"]):
                        self.add_one_element_to_operand_list("pip", (WhichClassForFeature.PKG, None))
                        self.add_one_element_to_operand_list("pip3", (WhichClassForFeature.PKG, None))
                    if self.does_first_operand_contain(["add"]):
                        self.add_one_element_to_operand_list("/etc", (WhichClassForFeature.FILESTD, make_other_io()))
