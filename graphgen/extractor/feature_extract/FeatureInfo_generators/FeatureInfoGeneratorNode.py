from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_input


class FeatureInfoGeneratorNode(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        operand_list = self.cmd_inv_after_io.operand_list
        length = len(operand_list)
        for index in range(length):
            operand = operand_list[index].get_name()
            if ".js" in operand:
                self.set_operand_element_by_index(index, (WhichClassForFeature.FILESTD, make_other_input()))
