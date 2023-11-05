from time import sleep

sleep(1)
print("START", flush=True)

while True:
    url = input()
    q = input()
    sleep(2)
    print("OUT")
    print(len(q), len(url))
    print("DONE", flush=True)
