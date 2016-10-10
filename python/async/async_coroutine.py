#!/usr/bin/env python3
import asyncio
import random

async def add(x, y):
    print('add(%(x)d, %(y)d')
    return x + y

async def mult(x, y):
    print('mult(%(x)d, %(y)d)' % {'x': x, 'y': y})
    await asyncio.sleep(random.randint(0,10))
    print('returning mult(%(x)d, %(y)d)' % {'x': x, 'y': y})
    return x * y

async def sum_of_products(a, b, c, d):
    tasks = [asyncio.ensure_future(mult(x, y))
             for x,y in [(a,c), (a,d), (b,c), (b,d)]]
    completed, pending = await asyncio.wait(tasks)
    result = sum([t.result() for t in completed])
    print(result)
    return result

async def foil(a, b, c, d):
    results = []
    for x,y in [(a,c), (a,d), (b,c), (b,d)]:
        results.append(await mult(x,y))
    result = (results[0], sum(results[1:3]), results[3])
    print(result)
    return result

loop = asyncio.get_event_loop()
loop.run_until_complete(sum_of_products(1,2,3,4))

