### Self-sign certificate proccess -

---

#### Creating CA -
 
 ```$ mkdir ~/openssl

 $ cd ~/openssl
 
 $ openssl req -x509 -new -nodes -key myCA.key -sha256 -days 3650 -out myCA.pem
 ```
 
#### Creating the certificate -

```$ openssl genrsa -out tls.key 2048

  * CN must match the DNS name of the route which is <EXAMPLE=(route name)-(prohect name).apps-crc.testing>

$ openssl req -new -key tls.key -out tls.csr
```

#### Self-signing the certificate -

```$ openssl x509 -req -in tls.csr -CA myCA.pem -CAkey myCA.key -CAcreateserial -out tls.crt -days 1650 -sha256

$ openssl x509 -in <cert file> -text -noout
```

