class TkPyBaseException(Exception):
    """TkPy基础错误"""
    pass

class TkPyProgramError(TkPyBaseException):
    """TkPy程序错误"""
    pass


class TkPyIdeError(TkPyProgramError):
    """TkPyIDE错误"""
    pass


class TkPyQtError(TkPyProgramError):
    """TkPy PyQt错误"""
    pass
