import jedi


def get_define_linenumber(source: str, line: int, column: int):
    script = jedi.Script(source, line, column)
    return script.completions()


if __name__ == '__main__':
    print(get_define_linenumber('import numpy', 1, len('import numpy')))
