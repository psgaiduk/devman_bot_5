def transliterate_text(text):
    if not text:
        return text
    if ' ' in text:
        text = text.replace(' ', '-')
    chars = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
             'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
             'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
             'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
             'ю': 'u', 'я': 'ya'}
    for char in text:
        if char.lower() in chars:
            text = text.replace(char, chars[char.lower()] if char.islower() else chars[char.lower()].title())

    return text
