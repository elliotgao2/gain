
class manipulation:
    @staticmethod
    def clean_string(s):
        """
            s = string to clean
            Clean tabs, spaces, newlines and unwanted Unicode characters
            Returns cleaned string
        """
        # Tuples can contain any method and argument length that you need to clean the string
        default_actions = (
            ('replace', '\n', ' '),
            ('replace', '\t', ' '),
            ('replace', '\r', ' '),
            ('strip',)
            )
        if isinstance(s, str):
            for method in default_actions:
                args = tuple(list(method)[1::])
                s = s.__getattribute__(list(method)[0])(*args)
            # Remove unnecessary spaces
            s = ' '.join(s.split())
            return s
        return s
