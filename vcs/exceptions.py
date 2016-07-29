class VersionError(Exception):
    def __init__(self, message, errors=None):
        super(VersionError, self).__init__(message)
        self.errors = errors