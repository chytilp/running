from dataclasses import dataclass, field


@dataclass
class Grade:
    grade: int
    from_: int
    to_: int
    from_equal: bool = True
    to_equal: bool = False
    time_convertible: bool = True

    def reverse(self) -> bool:
        return self.to_ < self.from_

    def match(self, value: int) -> bool:
        v = self.grade + value
        print(v)
        return True


@dataclass
class Grades:
    grades: dict[int, Grade] = field(default_factory=dict)

    @property
    def empty(self) -> bool:
        return len(self.grades) == 0

    def add(self, grade: Grade) -> None:
        if grade.grade < 1 or grade.grade > 5:
            raise ValueError(f"Grade {grade.grade} is out of range")
        self.grades[grade.grade] = grade

    def get_grade(self, grade: int) -> Grade | None:
        if grade < 1 or grade > 5:
            raise ValueError(f"Grade {grade} is out of range")

        return self.grades.get(grade)

    def grade_1(self) -> Grade | None:
        return self.grades.get(1)

    def grade_2(self) -> Grade | None:
        return self.grades.get(2)

    def grade_3(self) -> Grade | None:
        return self.grades.get(3)

    def grade_4(self) -> Grade | None:
        return self.grades.get(4)

    def grade_5(self) -> Grade | None:
        return self.grades.get(5)

    def get_dict(self) -> dict[int, tuple[int, int]]:
        return {
            1: (self.grade_1().from_, self.grade_1().to_),
            2: (self.grade_2().from_, self.grade_2().to_),
            3: (self.grade_3().from_, self.grade_3().to_),
            4: (self.grade_4().from_, self.grade_4().to_),
            5: (self.grade_5().from_, self.grade_5().to_),
        }

