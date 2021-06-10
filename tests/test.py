import os

username = os.popen('git config user.name').read().strip()
print(username)