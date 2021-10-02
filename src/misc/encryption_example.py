import base64
"""
Example base64 encrypted string
"""


# To b64 encrypt a token
token = "foo"
token_to_bytes = token.encode("ascii") #we have an encoded string
token_bytes_to_base64= base64.b64encode(token_to_bytes)#encoding bytes to base64
token_base64_encrypted_output = token_bytes_to_base64.decode('ascii')
print("\nEncrypted: " + str(token_base64_encrypted_output))

# To b64 decrypt a token
token_base64_encrypted_output = token_base64_encrypted_output.encode('ascii')
token_b64_output_bytes = base64.b64decode(token_base64_encrypted_output)
token_base64_decrypted_output = token_base64_decrypted_output.decode('ascii')
print("\nDecrypted: " + str(token_base64_decrypted_output))

#EOF