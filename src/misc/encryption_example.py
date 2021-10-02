import base64

"""
Example base64 encrypted string
"""
str_example = "foo"
str_to_bytes = str_example.encode("ascii") #we have an encoded string
bytes_to_base64= base64.b64encode(str_to_bytes)#encoding bytes to base64
base64_encrypted_output = bytes_to_base64.decode('ascii')
print("Encrypted: " + str(base64_encrypted_output))


base64_encrypted_output = base64_encrypted_output.encode('ascii')
b64_output_bytes = base64.b64decode(base64_encrypted_output)
base64_decrypted_output = b64_output_bytes.decode('ascii')
print("Decrypted: " + str(base64_decrypted_output))
