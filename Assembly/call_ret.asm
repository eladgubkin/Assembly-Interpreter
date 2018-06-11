call main
print eax
jmp End



calc:
    pop ebx
    pop ecx
    pop edx
    add ebx, ecx
    add ebx, edx
    mov eax, ebx
    ret



main:
    push 20
    push 40
    push 80
    call calc
    print eax




End: