from modeltranslation.translator import register, TranslationOptions, translator

from .models import News, Category


# 1-usul tarjima uchun
@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'body')


# # 2-usul tarjima uchun
# translator.register(News, TranslationOptions)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


# 13.10 daqiqasida qoldim