def hey(phrase):
    phrase = phrase.strip()
    if phrase == '':
        return "Fine. Be that way!"
    elif phrase.isupper():
        if phrase.endswith('?'):
            return "Calm down, I know what I'm doing!"
        else:
            return "Whoa, chill out!"
    elif phrase.endswith('?'):
        return "Sure."
    else:
        return "Whatever."