import re

from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from passlib.hash import pbkdf2_sha256

from my_library import constant
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
    widgets = {
      # 密码输入框
      Reader.password.field.name: forms.PasswordInput(),
    }

  def __init__(self, *args, **kwargs):
    super(ReaderAdminForm, self).__init__(*args, **kwargs)
    # 初始化时，密码字段设置为非必填，然后在 clean_password 中手动验证，因为编辑时，密码字段不填写则不修改密码
    self.fields[Reader.password.field.name].required = False

  def clean(self):
    # 验证读者编码
    Reader.gen_code()

  def clean_phone_number(self):
    """验证手机号"""
    phone_number = self.cleaned_data.get(Reader.phone_number.field.name)
    if phone_number and not re.match(constant.REGEX.phone_number, phone_number):
      raise forms.ValidationError('手机号格式错误！')
    return phone_number

  def clean_password(self):
    """编辑时验证密码是否为空"""
    if not self.instance.pk:
      password = self.cleaned_data.get(Reader.password.field.name)
      if not password:
        raise forms.ValidationError('这个字段是必填项。')
      return password
    # 返回原密码
    return self.instance.password


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
      # 新增用户，用户名为读者手机号，密码为读者密码
      User.objects.create_user(username=obj.phone_number, password=obj.password, first_name=obj.name)
    super().save_model(request, obj, form, change)


class BookAdmin(admin.ModelAdmin):
  list_display = field_name_by_model(Book.name, Book.authors, Book.publisher, Book.publish_time, Book.isbn, Book.cip, Book.language, Book.total_pages, Book.price)


admin.site.register(ReaderType, ReaderTypeAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BorrowRecord)

# TODO 保存用户时，如果用户名全数字，提醒去创建读者
