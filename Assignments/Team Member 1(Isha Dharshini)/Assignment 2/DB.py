import ibm_db
conn = ibm_db.connect("DATABASE = bludb; HOSTNAME = 19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT = 30699;SECURITY = SSL;SSLServerCertificate = DigiCertGlobalRootCA.crt; UID = ffx30903; PWD = DaKGipYjOtV83vvM ;","","")


print(conn)
print("Connection Successful") 





