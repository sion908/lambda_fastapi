class SimpleException(Exception):  # noqa: N818
    def __init__(self, status_code: int, msg: str):
        self.status_code = status_code
        self.msg = msg
