# import the module
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

while True:
    # the text to be transliterated
    text = str(input('Enter text to be translated: '))
    print('\n')
    # printing the transliterated text
    print('Hindi: ' + transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI))
    print('Telugu: ' + transliterate(text, sanscript.ITRANS, sanscript.TELUGU))
    print('Kannada: ' + transliterate(text, sanscript.ITRANS, sanscript.KANNADA))
    print('Tamil: ' + transliterate(text, sanscript.ITRANS, sanscript.TAMIL))
    print('Malayalam: ' + transliterate(text, sanscript.ITRANS, sanscript.MALAYALAM))
    print('Bengali: ' + transliterate(text, sanscript.ITRANS, sanscript.BENGALI))
    print('\n')