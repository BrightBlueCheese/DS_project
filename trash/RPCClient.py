from xmlrpc.client import ServerProxy

proxy = ServerProxy('http://localhost:3000')

if __name__ == '__main__':
    print(proxy.list_diectory(r'C:\Users\Las\OneDrive\Coding\Distributed_System\XMLRPC'))
