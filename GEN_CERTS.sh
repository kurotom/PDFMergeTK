#!/bin/bash

KEY="myprivatekey.key"
CSR="myrequest.csr"
CRT="mycertificate.crt"
PFX="mycertificate.pfx"
CERT_BASE64="mycert.pfx.base64"

# Genera una clave privada
openssl genrsa -out $KEY 2048

# Genera un archivo de solicitud de firma de certificado (CSR)
openssl req -new -key $KEY -out $CSR

# Genera un certificado autofirmado
openssl x509 -req -days 365 -in $CSR -signkey $KEY -out $CRT

# Combina la clave privada y el certificado en un archivo PFX
openssl pkcs12 -export -out $PFX -inkey $KEY -in $CRT

# Convertir a base64 para Github Secrets
base64 -w 0 $PFX > $CERT_BASE64

# Decodificar certificado
cat $CERT_BASE64 | base64 -d > $PFX

