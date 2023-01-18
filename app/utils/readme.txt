# You need to create a file in this folder called 'secrets.py'. Include the function below 
# in that file. The purpose of this file is to hold sensitive information that you don't want to 
# post publicly to GitHub.  This file is excluded from being sent to github by .gitignore. The
# function just returns a dictionary that holds your secrets. This is not secure if other people
# access to your computer and the files in your user account. 

def getSecrets():
    secrets = {
        'MAIL_PASSWORD':'YourPasswordHere',
        'MAIL_USERNAME':'YourEmailAddressHere',
        'MONGO_ADMIN': 'MongoUserNameHere',
        'MONGO_PASSWORD':'MongoPasswordHere'
        }
    return secrets