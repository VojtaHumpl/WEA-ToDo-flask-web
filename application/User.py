
"""
User class for the current user

Args:
    username (str): user's username used as identifier

Returns:
    User instance
"""
class User:
    def __init__(self, username: str):
        self.username = username
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        """
        User id getter

        Returns:
            str: username
        """
        return self.username

    