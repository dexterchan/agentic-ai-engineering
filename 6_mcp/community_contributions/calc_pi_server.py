import random
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("pi_calculator")



@mcp.tool()
async def calculate_pi_Leibniz(n: int) -> float:
    """ Calculate the value of pi using the Leibniz formula. """
    pi = 0.0
    cnt = 0
    while cnt < n:
        pi += ((-1) ** cnt) / (2 * cnt + 1)
        cnt += 1
    return pi * 4


@mcp.tool()
async def calculate_pi_random(n: int) -> float:
    """ Calculate the value of pi using a random method. But, it is very slow to converge. """
    inside_circle, cnt = 0, 0
    random.seed(42)  # For reproducibility
    while cnt < n:
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if x ** 2 + y ** 2 <= 1:
            inside_circle += 1
        cnt += 1
    return float(inside_circle) / n * 4


if __name__ == "__main__":
    # import asyncio
    # n = 1000000  # Number of iterations
    # pi_leibniz = asyncio.run(calculate_pi_Leibniz(n))
    # pi_random = asyncio.run(calculate_pi_random(n ))
    # print(f"Calculated Pi using Leibniz formula: {pi_leibniz}")
    # print(f"Calculated Pi using random method: {pi_random}")
    mcp.run(transport='stdio')
    