from re import sub as replace_all, MULTILINE, findall as search
from json import loads, dumps
from munch import DefaultMunch, Munch


class Parser:
    def __init__(self) -> None:
        pass

    def read(self, file: str):
        with open(file, "r") as content:
            return content.read()

    def parse(self, content: str):
        content = replace_all(
            r"(\s*)([0-9.A-Za-z]+):\s{\n", r'\1"\2": {\n', content, flags=MULTILINE
        )
        content = replace_all(
            r"(\s*)([0-9.A-Za-z]+):\s([0-9.A-Za-z\s]+)\n(\s*)}",
            r'\1"\2": "\3";;;\n\4}',
            content,
            flags=MULTILINE,
        )
        content = replace_all(
            r"(\s*)([0-9.A-Za-z]+):\s([0-9.A-Za-z\s]+)\n",
            r'\1"\2": "\3",\n',
            content,
            flags=MULTILINE,
        )
        content = replace_all(
            r'(\s*)}\n(\s*)"',
            r'\1},\n\2"',
            content,
            flags=MULTILINE,
        )
        content = content.replace(";;;", "")
        return content

    def evaluate(self, content: str):
        try: return DefaultMunch.fromDict(loads(self.parse(content)))
        except: pass

    def reConvert(self, db: Munch):
        fs_db = dumps(db.toDict(), indent=4).replace('"', "").replace(",", "")
        return fs_db

    def finalize(self, file: str, db: Munch):
        try:
            with open(file, "w") as opened_file:
                fs_db = dumps(db.toDict(), indent=4)
                fs_db = fs_db.replace('"', "").replace(",", "")
                opened_file.write(fs_db)
        except: pass