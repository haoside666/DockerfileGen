from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface

pkg_management_list = ["install", "in", "remove", "rm", "removeptf", "rmptf", "verify", "ve", "source-install", "si",
                       "install-new-recommends", "inr"]


class FeatureInfoGeneratorZypper(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        if self.get_operand_list_length() > 0:
            if self.does_first_operand_contain(pkg_management_list):
                self.all_but_first_operand_is_pkg()
