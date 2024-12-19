from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_input


class FeatureInfoGeneratorCargo(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.strip_startswith_is_hyphen_in_operand_list()
        if self.get_operand_list_length() > 0:
            command = self.get_first_operand_name_as_string()
            if command == "install":
                self.add_one_element_to_operand_list("Cargo.toml", (WhichClassForFeature.FILESTD, make_other_input()))

        self.add_one_element_to_operand_list("rust", (WhichClassForFeature.PKG, None))
        self.add_one_element_to_operand_list("cargo", (WhichClassForFeature.PKG, None))
