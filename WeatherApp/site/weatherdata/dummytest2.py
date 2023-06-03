
def GetPointOnGraph(varx):
    x = int(varx)
    return 25 * x + 5


def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b


# print(GetPointOnGraph(input("Enter x:")))
print(lerp(5, 0, 0.75))
