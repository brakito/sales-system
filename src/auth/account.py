import bcrypt

from src.db import useDataBase
from src.utils import notification, pause

class Account:
    def __init__(self):
        self.__userName = None
        self.__name = None
        self.__role = None
        self.__sessionActive = False

    def register (self, userName, password, name, role):
        createAdminProt = useDataBase('SELECT COUNT(*) FROM user')[0][0] == 0
        createUserProt = self.__sessionActive and self.getUserData()['role'] == 'admin'

        if createUserProt or createAdminProt:
            salt = bcrypt.gensalt()
            cryptPassword = bcrypt.hashpw(password.encode('utf-8'), salt)

            userId = useDataBase(
                'INSERT INTO user (userName, password, name, role) VALUES (?, ?, ?, ?)',
                (userName, cryptPassword, name, role),
                True
            )

            if not userId:
                notification("error", f"Wrong trying to add user {userName}.")
            else:
                notification("alert", f"User {userName} added whit role {role}.")
        else:
            notification("error", "Only admin acounts can create others Accounts")

    def login (self, userName, password):
        dbPassword = useDataBase(
            'SELECT password FROM user WHERE userName = ?',
            (userName,)
        )

        if len(dbPassword) == 1:
            if bcrypt.checkpw(password.encode('utf-8'), dbPassword[0][0]):
                # notification("alert", f"Welcome {userName}, you're login!")
                self.__openSession(userName)
                return True
        
        notification("alert", f"The userName and/or the password are incorrect!")
        return False
    
    def __openSession (self, userName):
        self.__sessionActive = True

        (user, name, role) = useDataBase(
            'SELECT userName, name, role FROM user WHERE userName = ?',
            (userName,)
        )[0]
        
        self.__userName = user
        self.__name = name
        self.__role = role
        
    def closeSession (self):
        self.__sessionActive = False

    def getUserData (self):
        if self.__sessionActive:
            return {
                'userName': self.__userName,
                'role': self.__role,
                'name': self.__name
            }
    
    def updateUserInfo (self, userName, password=None, name=None, role=None):
        if self.__sessionActive and self.getUserData()['role'] == 'admin':
            if password != None:
                salt = bcrypt.gensalt()
                newCryptedPassword = bcrypt.hashpw(password.encode('utf-8') ,salt)
                try:
                    useDataBase("UPDATE user SET password = ? WHERE userName = ?", (newCryptedPassword, userName))
                    notification("alert", "Password updated!")
                except:
                    notification("error", "Failed to update password")

            if name != None:
                try:
                    useDataBase("UPDATE user SET name = ? WHERE userName = ?", (name, userName))
                    notification("alert", "Name updated!")
                except:
                    notification("error", "Failed to update name")

            if role != None:
                try:
                    useDataBase("UPDATE user SET role = ? WHERE userName = ?", (role, userName))
                    notification("alert", "Role updated!")
                except:
                    notification("error", "Failed to update role")
        else:
            notification("error", "Only admin acounts can update users info")
    
    def deleteUser (self, userName):
        if self.__sessionActive and self.getUserData()['role'] == 'admin':
            try:
                useDataBase("DELETE FROM user WHERE userName = ?", (userName,))
                notification("alert", f"User {userName} deleted success")
            except:
                notification("error", "Delete user fail")
        else:
            notification("error", "Only admin acounts can delete users")

def createAdmin ():
    if useDataBase('SELECT COUNT(*) FROM user')[0][0] == 0:
        admin = Account()
        admin.register('admin', '4dmin', 'Admin', 'admin')
        notification("alert", "User name: 'admin', password: '4dmin'\nChange the password for security.")