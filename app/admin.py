import datetime

from django.contrib import admin
from django import forms

from .models import ReaderType, Reader, Book, BorrowRecord

# 管理页面顶部的文字
admin.site.site_header = '图书馆管理系统'
# 网站标题
admin.site.site_title = '图书馆管理系统'


def field_name_by_model(*fields):
  """
  获取模型字段（django.db.models.fields.Field）获取字段名称
  :param fields: 多个模型字段
  :return: 模型字段名称的元组
  """
  return tuple([item.field.name for item in fields])


# 自定义模型对应的管理页面
class ReaderTypeAdmin(admin.ModelAdmin):
  def render_valid_year(self, obj):
    """
    渲染 valid_year 字段：https://mozillazg.com/2013/04/django-admin-list_display-include-foreignkey.html
    :param obj: ReaderType 对象
    :return: valid_year 字段的值
    """
    return obj.valid_year if obj.valid_year > 0 else '永久'

  render_valid_year.short_description = '有效期（年）'

  # 列表显示字段
  list_display = field_name_by_model(ReaderType.name, ReaderType.can_borrow_book_num, ReaderType.can_borrow_days, ReaderType.can_renew_times, ReaderType.punish_rate) + (render_valid_year.__name__,)


class ReaderAdminForm(forms.ModelForm):
  """
  读者表单验证
  """

  class Meta:
    model = Reader
    fields = '__all__'

  def clean(self):
    Reader.gen_code()


class ReaderAdmin(admin.ModelAdmin):
  form = ReaderAdminForm
  # 排除编码字段，在后端生成，排除的模型字段 blank=False 不生效
  exclude = field_name_by_model(Reader.code)
  # 此处读者类型列会调用读者类型的 __str__ 方法
  list_display = field_name_by_model(Reader.code, Reader.name, Reader.sex, Reader.phone_number, Reader.reader_type)

  def save_model(self, request, obj, form, change):
    """
    保存模型
    :param request: 请求
    :param obj: 模型对象
    :param form: 表单
    :param change: 是否修改
    :return: None
    """
    # 新增非修改
    if not change:
      # 生成读者编码
      obj.code = Reader.gen_code()
    super().save_model(request, obj, form, change)


class BookAdmin(admin.ModelAdmin):
  list_display = field_name_by_model(Book.name, Book.authors, Book.publisher, Book.publish_time, Book.isbn, Book.cip, Book.language, Book.total_pages, Book.price)


admin.site.register(ReaderType, ReaderTypeAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BorrowRecord)
