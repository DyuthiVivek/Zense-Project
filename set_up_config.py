from configparser_crypt import ConfigParserCrypt

file = 'config.encrypted'
conf_file = ConfigParserCrypt()

# Setting up config file

# Create new AES key
conf_file.generate_key()
# Don't forget to backup your key somewhere
aes_key = conf_file.aes_key
print(aes_key)

conf_file.add_section('user')

# Add your credentials here
conf_file['user']['email'] = 'Your mail ID here'
conf_file['user']['pwd'] = 'Your password here'
conf_file['user']['assemblyAI'] = 'Your AssemblyAI API token here'

conf_file['user']['email_sender'] = 'ID of mail sender here'
conf_file['user']['sender_password'] = 'Password of mail sender here'

conf_file['user']['telegram'] = 'Your telegram token here'
    

# Write encrypted config file
with open(file, 'wb') as file_handle:
    conf_file.write_encrypted(file_handle)