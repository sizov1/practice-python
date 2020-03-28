for os in range (0, 255):
    if os > 96 and os < 123:
	    print(os, chr(os - 32))
    elif os > 64 and os < 91:
	    print(os, chr(os + 32))
    else:
        print(os, chr(os))