#!/usr/bin/env python3

import jwt  # pip install pyjwt
import argparse
import sys
import json
import datetime
import logging

def decode_JWT(inserted_token, key, audience=None):
    ''' Verifies and decodes token. Algorithm for decoding is established. '''
    try:
        decoded_token = jwt.decode(inserted_token, key, algorithms=['HS256'], audience=audience) #Specifies what to decode from JWT. 
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise Exception("You're token is expired.") #Error message for inspired token.
    except jwt.InvalidTokenError:
        raise Exception("Token is invalid.") #Error message for invalid token.

def decode_JWT_from_file(file_title, key, audience):
    ''' If JWT is in file, it is wrapped with decode_JWT. '''
    with open(file_title, 'r') as file:
        inserted_token = file.read() #File is opened with read permissions. 
        return decode_JWT(inserted_token, key, audience) #Specifies what to decode from JWT.

def check_admin(decrypted_token):
    ''' Sees if user's token contains admin privileges'''
    if 'Role' in decrypted_token and decrypted_token['Role'] == 'Admin':
        return True #The token is validated. 
    return False #Otherwise, the token is invalidated.

"""See whether or not the day is during the week."""
def is_weekday():
    current_date = datetime.date.today() #Looks for the current date.
    return current_date.weekday() < 5  # Checks to see if the day is during the week. 

'''Command line information is inputted.'''
def main():
    parser = argparse.ArgumentParser(description="JWT Decoder") #Activates the pasrser for the decoder.
    parser.add_argument('-t', '--token', required=True, help="JWT") #Input values for command line and arguments are added. 
    parser.add_argument('-s', '--secret', required=True, help="key")
    parser.add_argument('-i', '--input', required=False,  help="Information")
    parser.add_argument('-f', '--filename', required=False)
    parser.add_argument('-a', '--audience', required=False, help="Target demographic")
    arguments = parser.parse_args() #Parses the arguments. 

    try:
        decoded_token = decode_JWT(arguments.token, arguments.secret)
        if check_admin(decoded_token):
            logging.info("Decoding of JWT containing admin was successful.") #Accepts a valid admin token with no errors. 
            if is_weekday():
                logging.info("User is admin. It is a weekday.") #Verifies present admin privileges and if it's a weekday.
            else:
                logging.error("Error: This is the weekend.") #Access is denied on the weekends.
        else:
            logging.error("Error: token lacks admin privileges.") #Detects a token without proper credentials. 
    except Exception as e:
        print(f"Error: {e}") #Error message appears.
        sys.exit(1) #The 1 confirms there's an error while exiting. 

if __name__ == "__main__":
    main()
