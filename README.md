# pynmap
A serious(Tried to be) attempt to implement multi-threading to nmap module, which would result in faster scanning speed. I know that one can write NSE scripts for multi-threaded scanning with it, but I wanted to try it on python.

Result
======
Nmap Scanner uses 27 seconds to pingsweep from 192.168.0.1-255. But this script, use 5 seconds average to scan the same IP range with the same technique, the only thing different is, this uses Multi-Threading Technology.

![image of result](http://i.imgur.com/p0vCdo4.png)

Requirement
===========
1. Nmap module


This can be installed with pip, but the module file is already here, so there is no need to pip install it again.
