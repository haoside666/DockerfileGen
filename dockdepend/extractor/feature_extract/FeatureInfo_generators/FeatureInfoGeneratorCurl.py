from dockdepend.extractor.datatypes.AccessKindCommon import WhichClassForFeature, make_other_output
from dockdepend.extractor.feature_extract.FeatureInfo_generators.FeatureInfoGenerator_Interface import \
    FeatureInfoGeneratorInterface


class FeatureInfoGeneratorCurl(FeatureInfoGeneratorInterface):
    # Which ones do affect input/output?
    # -s affects output

    # Why curl can affect the generation of file stream information for subsequent commands?
    # example:
    #   curl -s ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/edirect.tar.gz | tar xzf -
    #   curl -sL "https://github.com/sbt/sbt/releases/download/v1.2.8/sbt-1.2.8.tgz" | gunzip | tar -x -C /usr/local
    #   echo $url|xargs curl -L -o airconnect.tar.gz
    def generate_info(self) -> None:
        operand_list = self.cmd_inv_after_io.operand_list
        if len(operand_list) == 1:
            if not self.does_flag_option_list_contain_specific_parameter("-o"):
                operand = operand_list[0].get_name()
                operand = operand.rpartition("/")[-1]
                operand_list[0].name = operand
                self.only_first_operand_is_other_output()
                self.pipe = operand
            else:
                option = self.get_specific_option_by_specific_parameter("-o")
                if option.option_arg == "-":
                    operand = operand_list[0].get_name()
                    operand = operand.rpartition("/")[-1]
                    self.pipe = operand
        elif len(operand_list) == 0:
            if self.does_flag_option_list_contain_specific_parameter("-o"):
                option = self.get_specific_option_by_specific_parameter("-o")
                operand = option.option_arg
                operand = operand.rpartition("/")[-1]
                self.pipe = operand
            else:
                if self.does_flag_option_list_contain_specific_parameter("--url"):
                    option = self.get_specific_option_by_specific_parameter("--url")
                    operand = option.option_arg
                    operand = operand.rpartition("/")[-1]
                    self.add_one_element_to_operand_list(operand, (WhichClassForFeature.FILESTD, make_other_output()))
                else:
                    pass
        else:
            if not self.does_flag_option_list_contain_specific_parameter("-o"):
                for index in range(len(operand_list)):
                    operand = operand_list[index].get_name()
                    if operand.startswith("https://") or operand.startswith("http://"):
                        operand = operand.rpartition("/")[-1]
                        self.add_one_element_to_operand_list(operand,
                                                             (WhichClassForFeature.FILESTD, make_other_output()))
            else:
                pass
