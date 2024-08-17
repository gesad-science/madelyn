class BadValueException(Exception):
    """Exception raised when some value is out of the business rule. 
       This exception contains a message with more details 
       and a flag "private" that says if the log is internal or not.
    """

    def __init__(self, detail, private = False, mask_detail = None) -> None:
        self.detail = detail
        self.private = private
        self.mask_detail = mask_detail
        super().__init__(detail)