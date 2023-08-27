from configparser_crypt import ConfigParserCrypt

file = 'config.encrypted' # filename
conf_file = ConfigParserCrypt()

# Set AES key
conf_file.aes_key = 'Paste your AES key here'
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
