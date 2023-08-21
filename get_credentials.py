from configparser_crypt import ConfigParserCrypt

file = 'config.encrypted' # filename
conf_file = ConfigParserCrypt()

# Set AES key
conf_file.aes_key = b'\xa1^\x03\xaa\xeb\xcc\x1aX\xd6\x1fAR.8\xfa\x9b\xfa3$\xf7\xad\x18\x05\xb2\xcf_\xa3\x03\xe3)\xd9H'
# Read from encrypted config file
conf_file.read_encrypted(file)

# Get user email
def get_email():
    return conf_file['user']['email']

# Get password
def get_pwd():
    return conf_file['user']['pwd']

# Get AssemblyAI API token
def get_assembyai_api():
    return conf_file['user']['assemblyAI']

# Get telegram token
def get_telegram_token():
    return conf_file['user']['telegram']

# Get email sender address
def get_sender_address():
    return conf_file['user']['email_sender']

# Get sender password
def get_sender_password():
    return conf_file['user']['sender_password']
