mov eax, 5
cmp eax, 5
jz Label1
jmp Label2

Label1:
    print 'EAX is 5!'
    jmp End
Label2:
    print 'EAX is not 5!'



End:




