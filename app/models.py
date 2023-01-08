from django.core.exceptions import ValidationError
from django.db import models

"""
模型字段参考：https://docs.djangoproject.com/zh-hans/4.1/ref/models/fields/
"""


class ReaderType(models.Model):
  """
  读者类型
  """

  def __str__(self):
    """
    在列表和详情页面，读者类型字段显示读者类型名称；
    在保存提示中，显示读者类型名称
    """
    return self.name

  # 元数据：https://docs.djangoproject.com/zh-hans/4.1/ref/models/options/
  class Meta:
    # 表名
    db_table = 'reader_type'
    # 对象名称
    verbose_name = '读者类型'
    # 对象复数名称
    verbose_name_plural = '读者类型'

  name = models.CharField("名称", max_length=255,
    # 不能为 null
    null=False,
    # 不能为空
    blank=False)
  can_borrow_book_num = models.IntegerField("可借书数量", null=False, default=1)
  can_borrow_days = models.IntegerField("可借书天数", null=False, default=1)
  can_renew_times = models.IntegerField("可续借次数", null=False, default=0)
  punish_rate = models.DecimalField("罚款率（元/天）",
    # 数字长度为 4，小数位数为 2
    max_digits=4, decimal_places=2,
    # 额外的 “帮助” 文本，随表单控件一同显示
    help_text="超过可借书天数后，每本每天多少钱")
  valid_year = models.IntegerField("有效期（年）", help_text="0 为永久有效", default=1)


class Reader(models.Model):
  """
  读者
  """

  def __str__(self):
    return '%s-%s' % (self.reader_type, self.name)

  class Meta:
    db_table = 'reader'
    verbose_name = '读者'
    verbose_name_plural = '读者'

  code = models.CharField('编码', max_length=255, null=False, blank=False)
  name = models.CharField('名称', max_length=255, null=False, blank=False)
  sex = models.BooleanField('性别', max_length=1, null=False, blank=False,
    # 会验证值是否在 choices 中，每个元组中的第一个元素是要在模型上设置的实际值，第二个元素是人可读的名称
    choices=((1, '男'), (2, '女')), default=1)
  reader_type = models.ForeignKey(ReaderType, verbose_name='读者类型', null=False,
    # 删除关联表规则
    on_delete=models.PROTECT,
    # 数据库约束，为 False 时表中实际上不会创建外键
    db_constraint=False)
  phone_number = models.CharField('手机号码', max_length=11, null=False, blank=False)
  password = models.CharField('密码', max_length=20, null=False, blank=False)

  @classmethod
  def gen_code(cls):
    """
    生成读者编码：年月日 + 数据库中最大的编码后四位 + 1
    """
    # 获取当前日期的年月日
    import datetime
    from django.db.models import Max
    from django.forms import forms

    date = datetime.datetime.now().strftime('%Y%m%d')
    # 获取数据库中最大的编码后四位
    max_code = Reader.objects.all().aggregate(Max('code'))['code__max']
    # 如果数据库中没有数据，max_code 为 None
    if max_code is None:
      max_code = 0
    else:
      # 截取编码后四位
      max_code = int(max_code[8:])
    # 如果编码后四位等于 9999，提示错误
    if max_code == 9999:
      raise forms.ValidationError('今日新增读者数量已达上限')
    return date + str(max_code + 1).zfill(4)


class Book(models.Model):
  """
  图书
  """

  def __str__(self):
    return '%s（%s）' % (self.name, self.authors)

  class Meta:
    db_table = 'book'
    verbose_name = '图书'
    verbose_name_plural = '图书'

  name = models.CharField('名称', max_length=255, null=False, blank=False)
  authors = models.CharField('作者', max_length=255, null=False, blank=False)
  publisher = models.CharField('出版社', max_length=255)
  publish_time = models.DateField('出版日期', null=False, blank=False)
  isbn = models.CharField('ISBN', max_length=255)
  cip = models.CharField('中图分类号', max_length=255, null=False, blank=False)
  language = models.BooleanField('语言', max_length=2, null=True, choices=((1, '中文'), (2, '英文'), (3, '日文'), (4, '俄文'), (5, '德文'), (6, '法文'), (99, '其他')))
  total_pages = models.IntegerField('总页数')
  price = models.DecimalField('价格（￥）', max_digits=10, decimal_places=2)


class BorrowRecord(models.Model):
  """
  借阅记录
  """

  class Meta:
    db_table = 'borrow_record'
    verbose_name = '借阅记录'
    verbose_name_plural = '借阅记录'

  reader = models.ForeignKey(Reader, verbose_name='读者', on_delete=models.PROTECT, db_constraint=False, null=False)
  book = models.ForeignKey(Book, verbose_name='图书', on_delete=models.PROTECT, db_constraint=False, null=False)
  renew_times = models.IntegerField('续借次数', default=0)
  created_times = models.DateTimeField('创建时间',
    # 创建时自动设置当前时间
    auto_now_add=True)
  plan_return_time = models.DateTimeField('应还时间')
  return_time = models.DateTimeField('实际还书时间')
  overdue_days = models.IntegerField('超期天数')
  overdue_amount = models.DecimalField('超期金额', max_digits=10, decimal_places=2, help_text='应罚款金额')
  publish_amount = models.DecimalField('罚款金额', max_digits=10, decimal_places=2)
  returned = models.BooleanField('是否已还书', max_length=1, null=True, default=False, choices=((True, '是'), (False, '否')))
