#!/bin/sh

if [ $# -ne 2 ]
  then
    echo "Please the Board and Server IPs"
    exit 0
fi

echo "Flushing the IPSEC SA and SP databases"
sudo ip xfrm state flush; sudo ip xfrm policy flush;

echo "Creating IPsec SA and SP databases on Server $2"
echo "Board IP: $1"
echo "Server IP: $2"

#SA - Board to Server
sudo ip xfrm state add src $1 dst $2 proto esp spi 0x5 reqid 0xabcd mode tunnel aead 'rfc4106(gcm(aes))' 0xc3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3 128

#SA - Server to Board
sudo ip xfrm state add src $2 dst $1 proto esp spi 0x100 reqid 0xef11 mode tunnel aead 'rfc4106(gcm(aes))' 0xc3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3 128

#SPDs
sudo ip xfrm policy add src $2 dst $1 dir out tmpl src $2 dst $1 proto esp reqid 0xef11 mode tunnel
sudo ip xfrm policy add src $1 dst $2 dir fwd tmpl src $1 dst $2 proto esp reqid 0xabcd mode tunnel
sudo ip xfrm policy add src $1 dst $2 dir in tmpl src $1 dst $2 proto esp reqid 0xabcd mode tunnel
