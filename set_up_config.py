from configparser_crypt import ConfigParserCrypt

file = 'config.encrypted'
conf_file = ConfigParserCrypt()

# Create new AES key
conf_file.generate_key()
# Don't forget to backup your key somewhere
aes_key = conf_file.aes_key
# Use like normal configparser class
conf_file.add_section('user')
conf_file['user']['email'] = 'Your mail ID here'
conf_file['user']['pwd'] = 'Your password here'


# Write encrypted config file
with open(file, 'wb') as file_handle:
    conf_file.write_encrypted(file_handle)