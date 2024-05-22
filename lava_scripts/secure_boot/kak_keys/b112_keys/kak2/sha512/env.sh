
openssl genrsa -out private_key_2048.pem 2048
openssl req -new -key private_key_2048.pem -out certificate_2048.csr -extensions v3_ca
openssl x509 -req -days 3650 -in certificate_2048.csr -signkey private_key_2048.pem -sha512  -out certificate_2048.crt
openssl x509 -in certificate_2048.crt -pubkey  -noout >publickey_extracted_from_cert.pem
openssl rsa -pubin -inform PEM -in publickey_extracted_from_cert.pem -outform DER -out publickey_extracted_from_cert.der
openssl dgst -sha512  publickey_extracted_from_cert.der


cp private_key_2048.pem kak_private_key.pem
cp certificate_2048.crt kak.crt
cp publickey_extracted_from_cert.pem kak_pubkey.pem
cp publickey_extracted_from_cert.der kak_pubkey.der

#cp kak_private_key.pem kak.crt kak_pubkey.pem kak_pubkey.der /ec-local/scratch/nilesh.waghmare/workspace/board_bringup/b0_bringup/clean_ws/build-tools/imgtools/keys/
