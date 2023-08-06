import unittest
from unittest.mock import Mock
import threading

class Group:
    def __init__(self, admin, admin_client):
        self.admin = admin
        self.admin_client = admin_client
        self.allMembers = {admin}
        self.joinRequests = {}
        self.waitClients = {}

def handshake(client):
    username = client.recv(1024).decode("utf-8")
    client.send(b"/sendGroupname")
    groupname = client.recv(1024).decode("utf-8")
    if groupname in groups:
        if username in groups[groupname].allMembers:
            groups[groupname].connect(username, client)
            client.send(b"/ready")
            print("User Connected:", username, "| Group:", groupname)
        else:
            groups[groupname].joinRequests.add(username)
            groups[groupname].waitClients[username] = client
            groups[groupname].sendMessage(username + " has requested to join the group.", "Shashwat's Chatsystem")
            client.send(b"/wait")
            print("Join Request:", username, "| Group:", groupname)
    else:
        groups[groupname] = Group(username, client)
        client.send(b"/adminReady")
        print("New Group:", groupname, "| Admin:", username)

class TestHandshake(unittest.TestCase):
    def test_handshake_existing_group_existing_user(self):
        mock_client = Mock()
        mock_client.recv.side_effect = [
            b"test_user",
            b"/sendGroupname",
            b"existing_group",
            b"/exit",
        ]
        global groups
        groups = {"existing_group": Group("admin_user", mock_client)}

        handshake(mock_client)

        self.assertEqual(mock_client.send.call_count, 2)  # There are 2 send calls

    def test_handshake_existing_group_new_user(self):
        mock_client = Mock()
        mock_client.recv.side_effect = [
            b"test_user",
            b"/sendGroupname",
            b"existing_group",
            b"/exit",
        ]
        global groups
        groups = {"existing_group": Group("admin_user", mock_client)}

        handshake(mock_client)

        self.assertEqual(mock_client.send.call_count, 2)  # There are 2 send calls

    def test_handshake_new_group(self):
        mock_client = Mock()
        mock_client.recv.side_effect = [
            b"test_user",
            b"/sendGroupname",
            b"new_group",
            b"/exit",
        ]
        global groups
        groups = {}

        handshake(mock_client)

        self.assertEqual(mock_client.send.call_count, 2)  # There are 2 send calls

if __name__ == '__main__':
    unittest.main()

