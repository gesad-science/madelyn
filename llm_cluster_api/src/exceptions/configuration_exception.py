class ConfigurationException(Exception):
    """
        Exception raised when some configuration goes wrong.
        When raised it should also shut down the api 

    """

    def __init__(self, detail) -> None:
        self.detail = detail
        super().__init__(detail)