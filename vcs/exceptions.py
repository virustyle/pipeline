class VersionError(Exception):
    def __init__(self, message, errors=None):
        super(EntityExist, self).__init__(message)
        self.errors = errors