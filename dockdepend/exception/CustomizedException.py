class ParsingException(Exception):
    def __init__(self, message='ParseError'):
        super(ParsingException, self).__init__(message)


class ExceptEndQuotemark(Exception):
    pass


class InstructFormatError(Exception):
    pass


class InstructNotFoundError(Exception):
    pass


class ParameterMissError(Exception):
    pass


class SyntaxNonSupportError(Exception):
    pass
