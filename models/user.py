class User:
    def __init__(self, user_id=None, first_name="", last_name="", age=0, grade=""):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.grade = grade
        self.test_session_id = None
        self.current_question = 0
        self.score = 0

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'grade': self.grade,
            'full_name': self.full_name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data.get('id'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            age=data.get('age'),
            grade=data.get('grade')
        )