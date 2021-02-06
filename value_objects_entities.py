from dataclasses import dataclass

# Value Object


@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str


Name("Harry", "Percival") != Name("Barry", "Percival")
# Names can change and do not have persistent identity

# Entity

# People do not change and have a persistent identity


class Person:
    def __init__(self, name: Name):
        name: name


harry = Person(Name("Harry", "Percival"))
barry = harry

barry.name = Name("Barry", "Percival")

assert harry is barry and barry is harry

# Value of name may change but Person entity remains identical
