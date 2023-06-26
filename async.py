import asyncio
import time

'''
async def pause(n):
    loop.run_in_executor(None, time.sleep, n)
    print(n)
    return n


async def main():
    futures = [asyncio.ensure_future(pause(i)) for i in range(0, 4)]
    result = await asyncio.gather(*futures)
    print(result)


loop = asyncio.get_event_loop()  
loop.run_until_complete(main()) 
loop.close() 
'''

class MyClass:
    async def async_method(self):
        await asyncio.gather(*(self.async_task(i) for i in range(5)))

    async def async_task(self, i):
        await asyncio.sleep(1)  # 비동기로 처리할 작업
        print(f'Iteration {i}')

async def main():
    obj = MyClass()
    await obj.async_method()

asyncio.run(main())



