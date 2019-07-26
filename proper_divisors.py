def proper_divisors():
    m = 10
    ret_message = ''
    pd_accum = 1

    while (m >0):
        try:
            m = int(input("Enter # (0 or less to quit)\n"))
        except ValueError:
            print("Invalid input, try again\n")
            continue

        for i in range(1, m-1):
            if (m % (m-i) == 0):
                pd_accum += (m - i)

        if (pd_accum > m):
            ret_message = "Abundant #\n"
        if (pd_accum < m):
            ret_message = "Deficient #\n"
        if pd_accum == m:
            ret_message = "Perfect #\n"
        if (m <= 0):
            ret_message = "Finished!\n"
        print(ret_message)
        pd_accum = 1

    if (m <= 0):
        return

proper_divisors()





