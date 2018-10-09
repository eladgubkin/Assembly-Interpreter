main:
    mov ecx, 7
    push ecx

    mov eax, 0

    call bit_counter

    pop eax
    print eax
    jmp End

bit_counter:
    mov eax, 0
    pop ecx

    Label:
        cmp ecx, 0
        jz return_to_main

        mov ebx, 1

        and ebx, ecx
        add eax, ebx

        shr ecx, 1
        jmp Label

    return_to_main:
        push eax
        ret

End: