mov eax, 0
mov ebx, 1

mov ecx, eax
add ecx, ebx

print eax
print ebx

Label:
    print ecx
    mov eax, ebx
    mov ebx, ecx

    mov ecx, eax
    add ecx, ebx

    cmp ecx, 987
    jz End

    jmp Label




End: