class InvalidCredentials(ValueError):
    def __init__(self, *args: object, detail="Invalid credentials") -> None:
        super().__init__(*args)
        self.detail = detail
