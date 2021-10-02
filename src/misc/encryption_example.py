import base64
"""
Example base64 encrypted string
"""

def main():
	"""
	1.)Copy API_TOKEN from OAuth & Permissions > Bot User OAuth Token (typically, the string
	begins with ‘xoxb-’).

	2.) Generate APP_TOKEN: Basic Information> App-Level Tokens> Generate Token and Scopes
	> token name: jarvis > Add scope > connections:write > click Generate. Copy APP_TOKEN
	from the new dialog box (typically, the string begins with ‘xapp-’) > click Done.
	"""

	# To b64 encrypt a token
	print("Enter your Slack API token (typically starts with \"xoxb\"): ")
	token = input()
	token_to_bytes = token.encode("ascii") #we have an encoded string
	token_bytes_to_base64= base64.b64encode(token_to_bytes)#encoding bytes to base64
	token_base64_encrypted_output = token_bytes_to_base64.decode('ascii')
	print("\nEncrypted Slack API Token: " + str(token_base64_encrypted_output))

	# To b64 decrypt a token
	token_base64_encrypted_output = token_base64_encrypted_output.encode('ascii')
	token_b64_output_bytes = base64.b64decode(token_base64_encrypted_output)
	token_base64_decrypted_output = token_b64_output_bytes.decode('ascii')
	print("\nDecrypted Slack API Token: " + str(token_base64_decrypted_output))


	print("Enter your Slack APP token (typically starts with \"xapp\"): ")
	token = input()
	token_to_bytes = token.encode("ascii") #we have an encoded string
	token_bytes_to_base64= base64.b64encode(token_to_bytes)#encoding bytes to base64
	token_base64_encrypted_output = token_bytes_to_base64.decode('ascii')
	print("\nEncrypted Slack APP Token: " + str(token_base64_encrypted_output))

	# To b64 decrypt a token
	token_base64_encrypted_output = token_base64_encrypted_output.encode('ascii')
	token_b64_output_bytes = base64.b64decode(token_base64_encrypted_output)
	token_base64_decrypted_output = token_b64_output_bytes.decode('ascii')
	print("\nDecrypted Slack APP Token: " + str(token_base64_decrypted_output))

main()

#EOF