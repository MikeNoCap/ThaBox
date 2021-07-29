import os
def client():
    if os.name == "nt":
        return os.system("python client/client.py")
    return os.system("python3 client/client.py")
