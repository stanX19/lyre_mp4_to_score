class A(dict):
    def f(self):
        pass
    def __str__(self):
        return "MemberOfA"


class B(A):
    pass


def k(a, b, c):
    print(a, b, c)

print(type(k))
k = k.__get__(A(), A)

print(type(k))
k("2", "3")

