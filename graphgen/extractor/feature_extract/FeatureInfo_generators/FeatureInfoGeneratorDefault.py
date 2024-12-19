from graphgen.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface
from graphgen.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_input, make_other_io
from graphgen.extractor.config.definitions import UNKNOWN_DIR_COMMAND_SET, IGNORE_COMMAND_SET


class FeatureInfoGeneratorDefault(FeatureInfoGeneratorInterface):
    def generate_info(self) -> None:
        self.all_operands_are_other()
        operand_list = self.cmd_inv_after_io.operand_list
        length = len(operand_list)
        for index in range(length):
            operand = operand_list[index].get_name()
            if "/" in operand or "." in operand:
                self.set_operand_element_by_index(index,
                                                  (WhichClassForFeature.FILESTD, make_other_io()))
        cmd_name = self.cmd_inv_after_io.cmd_name

        if cmd_name in UNKNOWN_DIR_COMMAND_SET:
            self.add_one_element_to_operand_list(".", (WhichClassForFeature.FILESTD, make_other_input()))
        elif "." in cmd_name or "/" in cmd_name:
            self.add_one_element_to_operand_list(cmd_name, (WhichClassForFeature.FILESTD, make_other_input()))
        if cmd_name not in IGNORE_COMMAND_SET:
            self.add_one_element_to_operand_list(f"unknown_{cmd_name}", (WhichClassForFeature.PKG, None))
