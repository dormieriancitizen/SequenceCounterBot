async def count(n):
    return n

async def fibonacci(n):
    
    if n == 0:
        return 0
    elif n == 1:
        return 1
    elif n == -1:
        return -1
    else:
        return (await fibonacci(n-1)) + (await fibonacci(n-2))

    # if n == -1:
    #     # Reset
    #     with open("fibonacci.txt", "w") as fibfile:
    #         fibfile.write("0\n1\n1")  # Corrected initial state
    #     return -1

    # with open("fibonacci.txt", "r") as fibfile:
    #     first = int(fibfile.readline())
    #     second = int(fibfile.readline())
    #     index = int(fibfile.readline())

    #     if n+1 < index and not n == -1:
    #         await fibonacci(-1)
    #         return (await fibonacci(n+1))

    #     if n == 0:
    #         return 0
    #     else:
    #         n -= 1

    #     x = second

    #     for i in range(n - index):
    #         x = first + second
    #         first = second
    # #         second = x

    # with open("fibonacci.txt", "w") as fibfile:
    #     fibfile.write(f"{first}\n{second}\n{n}")
    # return x

async def nsquared(n):
    return n**2

async def powersoftwo(n):
    return 2**n

sequences = {
    "n":count,
    "fibonacci":fibonacci,
    "n^2":nsquared,
    "2^n":powersoftwo
}