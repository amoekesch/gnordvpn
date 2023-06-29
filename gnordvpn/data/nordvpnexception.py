class NordVPNException(Exception):

    def __init__(self, message):
        self._message = self._clean(message)

    @property
    def message(self) -> str:
        return self._message


    def _clean(self, message) -> str:
        lines = []
        for line in message.splitlines():
            if len(line.strip()) > 1:
                lines.append(line.strip())
        return "".join(map(str, lines))


    def __str__(self) -> str:
        return self._message
