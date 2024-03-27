import os

def generate_random_bytes(length):
    return os.urandom(length)


def pars_sctp(bytes):
    print(bytes)
    source_port = int.from_bytes(bytes[0:2], 'big')
    destination_port = int.from_bytes(bytes[2:4], 'big')
    verification_tag = int.from_bytes(bytes[4:8], 'big')
    checksum = int.from_bytes(bytes[8:12], 'big')
    chunk_type = int.from_bytes(bytes[13:14], 'big')
    chunk_flags = int.from_bytes(bytes[14:15], 'big')
    chunk_length = int.from_bytes(bytes[15:17], 'big')
    if chunk_length > 4:
        data_end = 17 + chunk_length - 4
        chunk_value = int.from_bytes(bytes[17:data_end], 'big')
    else:
        chunk_value = None

    print(f'source_port = {source_port}\n'
          f'destination_port = {destination_port}\n'
          f'verification_tag = {verification_tag}\n'
          f'checksum = {checksum}\n'
          f'chunk_type = {chunk_type}\n'
          f'chunk_flags = {chunk_flags}\n'
          f'chunk_length = {chunk_length}\n'
          f'chunk_value = {chunk_value}')

pars_sctp(generate_random_bytes(1024))
