from dataclasses import dataclass
import random

# Value Object


@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str


assert Name("Harry", "Percival") != Name("Barry", "Percival")
# Names can change and do not have persistent identity

# Entity

# People do not change and have a persistent identity


class Person:
    def __init__(self, name: Name):
        self.name: name
        self.reference = f"Should be unique identifier: {random.random()}"

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        else:
            return self.reference == other.reference

    def __hash__(self):
        return hash(self.reference) # set to None if don't want to use in sets or dicts


harry = Person(Name("Harry", "Percival"))
barry = harry

barry.name = Name("Barry", "Percival")

assert harry is barry and barry is harry

# Value of name may change but Person entity remains identical

if __name__ == "__main__":
    assert harry is barry and barry is harry
    print(harry.__hash__())
    print(barry.__hash__())
