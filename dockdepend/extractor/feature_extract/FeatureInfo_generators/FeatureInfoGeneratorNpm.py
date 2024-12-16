from dockdepend.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from dockdepend.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_input


class FeatureInfoGeneratorNpm(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.strip_startswith_is_hyphen_in_operand_list()
        if self.get_operand_list_length() > 0:
            if self.does_first_operand_contain(["install", "i", "ci"]):
                self.all_but_first_operand_is_pkg()
                self.add_one_element_to_operand_list("package.json", (WhichClassForFeature.FILESTD, make_other_input()))
            elif self.does_first_operand_contain(["run"]):
                self.add_one_element_to_operand_list(".", (WhichClassForFeature.FILESTD, make_other_input()))

        self.add_one_element_to_operand_list("node", (WhichClassForFeature.PKG, None))
        self.add_one_element_to_operand_list("npm", (WhichClassForFeature.PKG, None))
