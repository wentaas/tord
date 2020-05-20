def case_insensitive(word: str):
    insensitive = [word.upper()]
    loop_range = range(len(word) - 1)
    for i in loop_range:
        c = word[:i] + word[i].upper() + word[i + 1:]
        insensitive.append(c)
        for n in loop_range:
            if n not in (i, loop_range):
                c = c[:n] + c[n].upper() + c[n + 1:]
                insensitive.append(c)
    return tuple(insensitive)


print(case_insensitive('tord'))
