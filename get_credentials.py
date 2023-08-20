from configparser_crypt import ConfigParserCrypt

file = 'config.encrypted' # filename
conf_file = ConfigParserCrypt()

# Set AES key
conf_file.aes_key = b'\x90H92{\xf2\xf6\x87f\xd7\xfa\xa0\x8dbf\xd9\xcc\x92\xcfm5\x9d\x16\xe0\xfb\x96\xd1\x95m6\xfau'

# Read from encrypted config file
conf_file.read_encrypted(file)

# Get user email
def get_email():
    return conf_file['user']['email']

# Get password
def get_pwd():
    return conf_file['user']['pwd']