from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_input


class FeatureInfoGeneratorGo(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        if self.get_operand_list_length() > 0:
            command = self.get_first_operand_name_as_string()
            if command == "mod":
                self.add_one_element_to_operand_list("go.mod", (WhichClassForFeature.FILESTD, make_other_input()))
            else:
                operand_list = self.cmd_inv_after_io.operand_list[1:]
                length = len(operand_list)
                for index in range(length):
                    operand = operand_list[index].get_name()
                    if "." in operand or "/" in operand:
                        self.set_operand_element_by_index(index + 1, (WhichClassForFeature.FILESTD, make_other_input()))
        self.add_one_element_to_operand_list("go", (WhichClassForFeature.PKG, None))
