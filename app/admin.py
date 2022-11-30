from django.contrib import admin

from .models import ReaderType, Reader, Book ,BorrowRecord


def model_to_list_display(need_model, add_items, subtract_items):
    '''*******使用此方法时，传递的need_model类不用使用三个"""来做注释，否则会获取到的是注释不是属性********
        need_model,     这个是需要生成的类
        add_items，      这个是需要增加的list列表
        subtract_items， 这个是需要减少的list列表
    '''
    ''' 这个方法主要是想一步生成list_display里面的元素，不用再一步一步的去敲''' \
        # 获取这个类的所有属性
    print('*' * 100)
    print(need_model.__doc__)
    print('*' * 100)
    doc_str = need_model.__doc__
    content_str = doc_str.split('(', 1)[-1][:-1]
    content_list = content_str.split(', ')
    # 如果需要屏蔽不显示的字段，可以在list时操作
    for item in subtract_items:
        if item in content_list:
            content_list.remove(item)
    for item in add_items:
        content_list.append(item)
    # 返回值需要list转元组
    return tuple(content_list)


# 自定义模型对应的管理页面
class ReaderTypeAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ('name', 'can_borrow_book_num', 'can_borrow_days', 'can_renew_times', 'punish_rate', 'valid_year')


# 在管理后台中加入应用模型
admin.site.register(ReaderType, ReaderTypeAdmin)
admin.site.register(Reader)
admin.site.register(Book)
admin.site.register(BorrowRecord)