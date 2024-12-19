from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_input


class FeatureInfoGeneratorMvn(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        if self.get_operand_list_length() > 0:
            command = self.get_first_operand_name_as_string()
            if command == "install" or command == "clean":
                self.add_one_element_to_operand_list("pom.xml", (WhichClassForFeature.FILESTD, make_other_input()))

        self.add_one_element_to_operand_list("mvn", (WhichClassForFeature.PKG, None))
        self.add_one_element_to_operand_list("java", (WhichClassForFeature.PKG, None))
