#!/usr/bin/env python
import argparse
import os

#domain_file = '/Users/isafronov/Desktop/23/domains_eugene.txt'
#out_file = '/Users/isafronov/Desktop/23/urls.txt'

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle

#arguments
parser = argparse.ArgumentParser(description='Takes the list of domains and gets screenshots of web services running on them (80,443 ports)')
parser.add_argument("-i", dest="infile", required=False,
                    help="input file with domains,one domain per line", metavar="FILE",
                    type=lambda x: is_valid_file(parser, x))
parser.add_argument("-o", dest="outfile", required=False, default=(os.getcwd()+'/urls.txt'),
                    help="file to output all urls", metavar="FILE")
parser.add_argument("-c", dest="configfile", required=False, default=(os.getcwd()+'/config.yml'),
                    help="screenshotconfig file", metavar="FILE")
parser.add_argument(dest="infile")

args = parser.parse_args()



#check if file exists


def domains_to_urls(arr_of_domains):
    url_list = []
    with open(args.outfile,'w') as out:
        for elem in arr_of_domains:
            if elem[2]:
                if elem[1] == 80:
                    line = 'http://'+elem[0]+'\n'
                    url_list.append(line)
                    out.write(line)
                if elem[1] == 443:
                    line = 'https://'+elem[0]+'\n'
                    url_list.append(line)
                    out.write(line)
    return url_list


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

def write_config(_url_list):
    #copy default config to new config
    with open(os.path.dirname(os.path.abspath(__file__))+'/default_config.yml','r') as default_config:
        with open(args.configfile, 'w') as config_file:
            for line in default_config:
                config_file.write(line)
            for line in _url_list:
                config_file.write(' '+line)
    return






if __name__ == '__main__':
    with open(args.infile) as f:
        results = check_if_http(f.read().splitlines(),[80,443])
        url_list = domains_to_urls(results)
        write_config(url_list)





