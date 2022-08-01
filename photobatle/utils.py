from transliterate import translit


class DataMixin:
    def slug_russian_word(self, word):
        # Making a slug of Russian words
        russia = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        slug = ''
        for i in word:
            if i.lower() in russia:
                slug += translit(i, language_code='ru', reversed=True)
            else:
                if i == ' ':
                    slug += '-'
                else:
                    slug += i
        return slug
