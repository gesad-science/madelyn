class BusinessRuleException(Exception):
    """Exception raised when some value is out of the business rules. 
       This exception contains a message with more details 
       and a flag "private" that says if the log is internal or not.
       In case "private" is true, its also expected to receive a
       other message text that is displayed in case you want to hide 
       the real message from non-developers 
    """

    def __init__(self, detail, private = False, mask_detail = None) -> None:
        self.detail = detail
        self.private = private
        self.mask_detail = mask_detail
        super().__init__(detail)