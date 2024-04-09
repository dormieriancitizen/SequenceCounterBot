async def count(n):
    return n

async def fibonacci(n):
    if n == -1:
        # Reset
        with open("fibonacci.txt", "w") as fibfile:
            fibfile.write("0\n1\n1")  # Corrected initial state
        return -1

    with open("fibonacci.txt", "r") as fibfile:
        first = int(fibfile.readline())
        second = int(fibfile.readline())
        index = int(fibfile.readline())

        if n < index:
            fibonacci(-1)
            fibonacci(n)

        if n == 0:
            return 0
        else:
            n -= 1

        x = second

        for i in range(n - index):
            x = first + second
            first = second
            second = x

    with open("fibonacci.txt", "w") as fibfile:
        fibfile.write(f"{first}\n{second}\n{n}")
    return x

async def powersoftwo(n):
    return n**2

sequences = {
    "n":count,
    "fibonacci":fibonacci,
    "n^2":powersoftwo
}