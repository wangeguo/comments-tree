class Error(Exception):
    status_code = 400
    error_code = 000000

    def __init__(self, status_code, error_code, message, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.payload = payload

    def to_dict(self):
        return {
            "code": self.error_code,
            "message": self.message,
            "errors": dict(self.payload or ())
        }


""" Custom Business Exception"""

# User

IncorrectUsernameError = Error(400, 100000, "Incorrect username error")
IncorrectPasswordError = Error(400, 100001, "Incorrect password error")
UserAlreadyExistsError = Error(400, 100002, "User already exists error")


def RegisterValidateError(errors):
    return Error(400, 100003, "Invalid registration error", errors)


def LoginValidateError(errors):
    return Error(400, 100004, "Invalid login error", errors)


LoginRequiredError = Error(401, 100005, "Login required error")

# Post
PostNotExistError = Error(404, 101000, "Post not exist error")


def CreatePostValidateError(errors):
    return Error(400, 101001, "Create post validation Error", errors)


def UpdatePostValidateError(errors):
    return Error(400, 101002, "Update post validation Error", errors)


def ReplyPostValidateError(errors):
    return Error(400, 101003, "Reply post validation Error", errors)


AuthorRequiredError = Error(403, 101004, "Author required error")
PostNotFoundError = Error(404, 101005, "Post not found error")
