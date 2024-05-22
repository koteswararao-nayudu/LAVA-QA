import zipfile
import xml.etree.ElementTree as ET
import subprocess
import argparse
import os
import sys
import base64
import datetime
import time
import traceback
import io

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
import base64
import math

class Encryption:
    def __init__(self, private_key_path):
        self.private_key_path = private_key_path
        self.public_key_path = ''
        # self.chunk_size=1024*1000*32
        # self.small_file_size=1024*1000*40
        self.chunk_size=1024*1000*175
        self.small_file_size=1024*1000*120
        self.load_private_key(self.private_key_path)
        # self.load_public_key(self.public_key_path)
        # self.create_fernet()

    def load_public_key(self, public_key_path):
        with open(public_key_path, "rb") as key_file:
            public_key_data = key_file.read()
            public_key = serialization.load_pem_public_key(
                public_key_data,
                backend=default_backend()
            )
            self.public_key = public_key

    def load_private_key(self, private_key_path):
        with open(private_key_path, "rb") as key_file:
            private_key_data = key_file.read()
            private_key = serialization.load_pem_private_key(
                private_key_data,
                password=None,
                backend=default_backend()
            )
            self.private_key = private_key

    def create_fernet(self):
        symmetric_key = os.urandom(32)
        self.symmetric_key = symmetric_key
        base64_key = base64.urlsafe_b64encode(symmetric_key)
        self.fernet = Fernet(base64_key)

        # Encrypt the symmetric key with the public key
        self.encrypted_key = self.public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def encrypt_file(self, input_file_path, encrypted_file_path):
        self.create_fernet()

        with open(input_file_path, 'rb') as input_file:
            with open(encrypted_file_path, 'wb') as encrypted_file:
                # Write the encrypted symmetric key at the beginning of the file
                encrypted_file.write(self.encrypted_key)

                while True:
                    chunk = input_file.read(self.chunk_size)
                    if not chunk:
                        break
                    encrypted_chunk = self.fernet.encrypt(chunk)
                    encrypted_file.write(encrypted_chunk)

        print("Encryption finished!!")

    def decrypt_file(self, encrypted_file_path, decrypted_file_path, count):
        # print("Inside decrypt_file: "+encrypted_file_path)
        # print("Inside decrypt_file: "+decrypted_file_path)
        with open(encrypted_file_path, 'rb') as encrypted_file:
            #if (count == 0):
            # Read the encrypted symmetric key from the beginning of the file
            encrypted_key = encrypted_file.read(256)
            # print("Read key from file: "+str(encrypted_key))
            # Decrypt the symmetric key with the private key
            symmetric_key = self.private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Create Fernet instance with the decrypted symmetric key
            base64_key = base64.urlsafe_b64encode(symmetric_key)
            self.fernet = Fernet(base64_key)

            with open(decrypted_file_path, 'wb') as decrypted_file:
                while True:
                    chunk = encrypted_file.read(self.chunk_size)
                    if not chunk:
                        break
                    decrypted_chunk = self.fernet.decrypt(chunk)
                    decrypted_file.write(decrypted_chunk)


    def split_to_small(self, file_path, splitted_file_name_path):
        file_name = os.path.basename(file_path)
        dir_name = os.path.dirname(file_path)
        file_size = os.path.getsize(file_path)

        with open(file_path, 'rb') as f:
            chunk = f.read(self.small_file_size)
            index = 0
            while chunk:
                index += 1
                split_file_path = os.path.join(dir_name, f'{file_name}.part{index}')
                with open(split_file_path, 'wb') as out_file:
                    out_file.write(chunk)
                with open(os.path.join(dir_name, splitted_file_name_path), 'a') as txt_file:
                    txt_file.write(f'{split_file_path}\n')
                chunk = f.read(self.small_file_size)
        print("Splitting the encrypted file into small files!!")

    def merge_to_big(self, file_name_list_path, merged_file_path, target_path):
        with open(file_name_list_path) as f:
            file_list = f.read().splitlines()
        with open(merged_file_path, 'wb') as merged_f:
            for file_path in file_list:
                # print("local to merge file: ",file_path)
                with open(target_path+"/"+file_path, 'rb') as f:
                    # print("start to merge file: ",target_path+"/"+file_path)
                    time.sleep(0.1)
                    merged_f.write(f.read())
 


    
    def old_merge_to_big(self, file_name_list_path, merged_file_path, original_file_path):
        with open(file_name_list_path) as f:
            file_list = f.read().splitlines()
        with open(merged_file_path, 'wb') as merged_f:
            for file_path in file_list:
                with open(file_path, 'rb') as f:
                    merged_f.write(f.read())
        if subprocess.call(["cmp", "-s", original_file_path, merged_file_path]) == 0:
            print(f"The decrypted file is same as input file")
        else:
            print(f"The decrypted file is different from input file")

    def encrypt_files(self, file_name_list_path, encrypted_file_name_list_path):
        with open(file_name_list_path) as f, open(encrypted_file_name_list_path, 'w') as out_f:
            for line in f:
                orig_file_path = line.strip()
                encrypted_file_path = f"{orig_file_path}.encrypted"
                self.encrypt_file(orig_file_path, encrypted_file_path)
                out_f.write(f"{encrypted_file_path}\n")

    def decrypt_files(self, encrypted_file_name_list_path, decrypted_file_name_list_path, target_path, decrypted_component_path):
        # print("Start to decrypt ....")
        with open(encrypted_file_name_list_path) as f, open(decrypted_file_name_list_path, 'w') as out_f:
            count = 0
            for line in f:
                encrypted_file_path = line.strip()
                # print("Current encrypted small file name:"+encrypted_file_path)
                decrypted_file_path = f"{encrypted_file_path}.decrypted"
                # print("Current decrypted small file name:"+decrypted_file_path)
                self.decrypt_file(target_path+"/"+encrypted_file_path, decrypted_component_path+"/"+decrypted_file_path, count) 
                subprocess.call(["sync"])
                out_f.write(f"{decrypted_file_path}\n")
                count += 1
        print("Decryption finished!!")

    def removed_components(self, file_name_list_path):
       # print("Start to decrypt ....")
        with open(file_name_list_path) as f:
            count = 0
            for line in f:
                encrypted_file_path = line.strip()
                # print("Remove current encrypted small file name:"+encrypted_file_path)
                subprocess.call(["rm", "-f", target_path+"/"+encrypted_file_path])
                count += 1
        # print("Remove encrypted files!!")

default_download_sub='/ota_tmp/edgeQ_ota/tools'
default_image_name='target.tar.gz'
default_download_file='sw_release_package.zip'
default_manifest_xml='manifest.xml'
default_decryped_image_name='decryped_release_package.zip'
default_speed_limit="0"

splitted_file_name_path = 'splitted_file_name.txt'
encrypted_file_name_list_path = 'encrypted_file_name_list.txt'
decrypted_file_name_list_path = 'decrypted_file_name_list.txt'
decrypted_component_path='/ota_tmp/edgeQ_ota/tools'
def verify_signature(pem_key_file, image_file, signature):
    # Read the public key from file

    with open(pem_key_file, 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
    
    # Read the file to verify signature as binary data in chunks
    chunk_size = 1024*20
    hasher = hashes.Hash(hashes.SHA256(), backend=default_backend())
    with open(image_file, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)
    hash_value = hasher.finalize()
    # print("Public image hash value:")
    # print(hash_value)
    '''
    # Verify the signature
    if (hash_value == signature):
        print("Signature is valid")
        return True
    else:
        print(f"InvalidSignature error: "+signature)
        return False
    '''

    try:
        public_key.verify(
            signature,
            hash_value,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Signature is valid")
        return True
    except InvalidSignature as e:
        print(f"InvalidSignature error: {e}")
        print(traceback.format_exc())
        return False


def split_url(url):
    if url.startswith("http:"):
        return ("http", url)
    elif url.startswith("sftp:"):
        return ("sftp", url[5:])
    elif url.startswith("scp:"):
        return ("scp", url[4:])
    else:
        raise ValueError("Invalid URL: " + url)

def download_distribute_files(http_path, download_file_name, download_password, limit_rate):
    #create the tmp download space for downloading
    if os.path.exists(default_download_sub):
        print ("Download sub-directory exists")
    else:
        # print("Download sub-directory doesn't exist")
        mk_command=["sudo", "mkdir", "-p", "{}".format(default_download_sub)]
        subprocess.run(mk_command)
        # tmpfs_command=["sudo", "mount", "-t", "tmpfs", "-o" "size=3G", "tmpfs" "{}".format(default_download_sub)]
        # subprocess.run(tmpfs_command)
    # cd_command=["cd", "{}".format(default_download_sub)]
    # subprocess.run(cd_command)

    if (os.path.isfile(download_file_name)):
        rm_command=["sudo", "rm", "{}".format(download_file_name)]
        subprocess.run(rm_command)
    
    download_path_and_file=http_path+"/"+download_file_name
    if limit_rate == '0':
        '''
        print (" download ip, path and file: "+download_path_and_file)
        print (" user and password: "+ download_password)
        print (" target file name: "+download_file_name)
        '''
        command = ["sudo", "curl", download_path_and_file, "-o", default_download_sub+"/"+download_file_name, "-u", download_password]
    else:
        # print ("Speed limit: "+limit_rate)
        command = ["curl",  "--limit-rate", limit_rate , download_path_and_file, "-o", default_download_sub+"/"+download_file_name, "-u", download_password]
    
    download_result = subprocess.run(command)

    #subprocess.run("sudo mv ./{0} {1}".format(download_file_name,default_download_sub))
    # mv_command = ["sudo", "mv", "{0}".format(download_file_name), "{0}".format(default_download_sub)]
    # subprocess.run(mv_command)
    # print("Complete the release package downloading and move to {}".format(default_download_sub))
    return download_result

def check_download_validation(public_key_file, image_file_name, manifest_xml_file):

    # extract the zip file
    # with zipfile.ZipFile(download_file_name, 'r') as zip_ref:
    #    zip_ref.extractall('unpacked')
    # distribute the files to differen folders

    # read the product information from the XML file
    tree = ET.parse(manifest_xml_file)
    root = tree.getroot()
    # print("manifest signature: {}".format(root.find('signature').text))
    signature = base64.b64decode(root.find('signature').text)
    with open("public_signature.bin",'wb') as f:
        f.write(signature)
    #public_key_file = root.find('public_key').text

    # call verify_signature to verify the signature
    return verify_signature(public_key_file, image_file_name, signature)

if __name__ == "__main__":
    # print("Start to run client manifest decoding and validation check!")
	# Get the current date and time
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")

    parser = argparse.ArgumentParser(description='''Client manifest utility!''')
    parser.add_argument('--operation', type=str, default="", action="store", dest='current_op', help='Client manifest utility operation {download_package|download_validation}')
    parser.add_argument('--http_path', type=str, default="", action="store", dest='http_path', help='Enter http path for package release, such as { http://192.168.103.1:8000/srv/tftp/sw_release/ }')
    parser.add_argument('--download_file_name', type=str, default=default_download_file, action="store", dest='download_file_name', help='Enter download file name of current release package, not include the path')
    parser.add_argument('--pem_file', type=str, default="", action="store", dest='pem_file', help='Enter the pem file name, which includes the path')
    parser.add_argument('--image_name', type=str, default=default_image_name, action="store", dest='current_image_name', help='Enter the image name {default is IMAGE.tar.gz}, include path')    
    parser.add_argument('--manifest_xml_file', type=str, default=default_manifest_xml, action="store", dest='manifest_xml', help='Enter the manifest file name, include path')
    parser.add_argument('--download_password', type=str, default="", action="store", dest='download_password', help='Enter the download password')
    parser.add_argument('--decrypted_file', type=str, default=default_decryped_image_name, action="store", dest='flaintext_image_name', help='Enter the decrypted flaintext name {default is decryped_release_package.zip}, include path')    
    parser.add_argument('--limit-rate', type=str, default=default_speed_limit, action="store", dest='limit_rate', help='Enter the limit-rate value from shell script')

    args=parser.parse_args()
    print("Build date: "+date_str)
    # print("The current arguments: op:"+args.current_op+", release root path:"+args.http_path+", pem_file:"+args.pem_file+", default image name:"+args.current_image_name+", manifest file name:"+args.manifest_xml)
    # print("Current limit rate: "+args.limit_rate)
    '''
    Based on the input arguments to determine the features of invoking
    '''
    current_op=args.current_op
    if current_op == 'download_package':
        http_path=args.http_path
        download_file_name=args.download_file_name
        download_password=args.download_password
        limit_rate=args.limit_rate.replace(" ", "")
        download_result=download_distribute_files(http_path, download_file_name, download_password, limit_rate)
    elif current_op == 'download_validation':
        pem_file=args.pem_file
        current_image_name=args.current_image_name
        manifest_xml=args.manifest_xml
        if (os.path.isfile(pem_file)):
            if check_download_validation(pem_file,current_image_name, manifest_xml):
                sys.exit(0)
            else:
                sys.exit(625)
        else:
            print("pem file doesn't exist, please input the correct pem file, include path and file")
            sys.exit(625)
    elif current_op == 'download_decryption':
        pem_file=args.pem_file
        current_image_name=args.current_image_name
        current_decrypted_image_name=args.flaintext_image_name
        target_path=os.path.dirname(current_image_name)
        # print ("Current download file and path: "+current_image_name)
        # print("Current target path: "+target_path)
        encryption = Encryption(pem_file)
        if (os.path.isfile(pem_file)):
            print("Start to decrypt the downloaded file....")
            subprocess.call(["rm", "-rf", decrypted_file_name_list_path])
            subprocess.call(["rm", "-rf", current_decrypted_image_name])
            subprocess.call(["tar", "-xzf", current_image_name, "-C", target_path])
            subprocess.run(["sync"])
            subprocess.call(["rm", "-rf", current_image_name])
            encryption.decrypt_files(target_path+"/"+encrypted_file_name_list_path, target_path+"/"+decrypted_file_name_list_path, target_path, decrypted_component_path)
            # print("Start to merge to final file")
            encryption.removed_components(target_path+"/"+encrypted_file_name_list_path)
            subprocess.run(["sync"])
            # sys.exit(1)
            encryption.merge_to_big(target_path+"/"+decrypted_file_name_list_path, current_decrypted_image_name, decrypted_component_path)
            encryption.removed_components(target_path+"/"+decrypted_file_name_list_path)
        else:
            print("pem file doesn't exist, please input the correct pem file, include path and file")
            sys.exit(625)
    else:
        print ("Please select one of {download_package|download_validation}")
        sys.exit(622)