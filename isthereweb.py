domain_file = '/Users/isafronov/Desktop/23/domains_eugene.txt'
out_file = '/Users/isafronov/Desktop/23/urls.txt'



def domains_to_urls(arr_of_domains):
    with open(out_file,'w') as out:
        for elem in arr_of_domains:
            if elem[2]:
                if elem[1] == 80:
                    out.write('http://'+elem[0]+'\n')
                if elem[1] == 443:
                    out.write('https://'+elem[0]+'\n')
    return


def check_if_http(dests,ports):
    import asyncio
    import time

    now = time.time()

    async def check_port(ip, port, loop):
            conn = asyncio.open_connection(ip, port, loop=loop)
            try:
                    reader, writer = await asyncio.wait_for(conn, timeout=3)
                    print(ip, port, 'ok')
                    return (ip, port, True)
            except:
                    print(ip, port, 'nok')
                    return (ip, port, False)

    async def run(dests, ports, loop):
            tasks = [asyncio.ensure_future(check_port(d, p, loop)) for d in dests for p in ports]
            responses = await asyncio.gather(*tasks)
            return responses


    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(dests, ports, loop))
    loop.run_until_complete(future)
    print('#'*50)
    print('Results: ', future.result())
    print('#'*50)
    print('Total time: ', time.time() - now)
    return future.result()



with open(domain_file) as f:
    results = check_if_http(f.read().splitlines(),[80,443])

domains_to_urls(results)




