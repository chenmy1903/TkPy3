import sys
import traceback


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


class NoLexerError(TkPyProgramError):
    """没有高亮"""
    pass


class NoSetupError(TkPyIdeError):
    pass



def get_error():
    sys.last_type, sys.last_value, last_tb = ei = sys.exc_info()
    sys.last_traceback = last_tb
    try:
        lines = traceback.format_exception(ei[0], ei[1], last_tb.tb_next)
        if sys.excepthook is sys.__excepthook__:
            error_message = ''.join(lines)
            return error_message
        else:
            sys.excepthook(ei[0], ei[1], last_tb)
    finally:
        last_tb = ei = None
