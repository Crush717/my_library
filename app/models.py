from django.db import models

"""
模型字段参考：https://docs.djangoproject.com/zh-hans/4.1/ref/models/fields/
"""


class ReaderType(models.Model):
  """
  读者类型
  """

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
  valid_year = models.IntegerField("有效期（年）", help_text="0 为永久有效")


class Reader(models.Model):
  """
  读者
  """

  class Meta:
    db_table = 'reader'
    verbose_name = '读者'
    verbose_name_plural = '读者'

  code = models.CharField('编码', max_length=255, null=False, blank=False)
  name = models.CharField('名称', max_length=255, null=False, blank=False)
  sex = models.CharField('性别', max_length=1, null=False, blank=False,
                         # 会验证值是否在 choices 中，每个元组中的第一个元素是要在模型上设置的实际值，第二个元素是人可读的名称
                         choices=((1, '男'), (2, '女')))
  reader_type = models.OneToOneField(ReaderType, verbose_name='读者类型', null=False,
                                     # 删除关联表规则
                                     on_delete=models.DO_NOTHING,
                                     # 虚拟外键，表中实际上不会创建外键
                                     db_constraint=True)
  phone_number = models.CharField('手机号码', max_length=11, null=False, blank=False)


class Book(models.Model):
  """
  图书
  """

  class Meta:
    db_table = 'book'
    verbose_name = '图书'
    verbose_name_plural = '图书'

  code = models.CharField('编码', max_length=255, null=False, blank=False)
  name = models.CharField('名称', max_length=255, null=False, blank=False)
  authors = models.CharField('作者', max_length=255, null=False, blank=False)
  publisher = models.CharField('出版社', max_length=255)
  publish_time = models.DateTimeField('出版日期', null=False, blank=False)
  isbn = models.CharField('ISBN', max_length=255)
  catalog = models.CharField('分类号', max_length=255, null=False, blank=False)
  language = models.CharField('语言', max_length=2, null=True, choices=((1, '中文'), (2, '英文'), (3, '日文'), (4, '俄文'), (5, '德文'), (6, '法文'), (99, '其他')))
  total_pages = models.IntegerField('总页数')
  price = models.DecimalField('价格', max_digits=10, decimal_places=2)


class BorrowRecord(models.Model):
  """
  借阅记录
  """

  class Meta:
    db_table = 'borrow_record'
    verbose_name = '借阅记录'
    verbose_name_plural = '借阅记录'

  reader = models.OneToOneField(Reader, verbose_name='读者', on_delete=models.DO_NOTHING, db_constraint=True, null=False)
  book = models.OneToOneField(Book, verbose_name='图书', on_delete=models.DO_NOTHING, db_constraint=True, null=False)
  renew_times = models.IntegerField('续借次数', default=0)
  created_times = models.DateTimeField('创建时间',
                                       # 创建时自动设置当前时间
                                       auto_now_add=True)
  plan_return_time = models.DateTimeField('应还时间')
  return_time = models.DateTimeField('实际还书时间')
  overdue_days = models.IntegerField('超期天数')
  overdue_amount = models.DecimalField('超期金额（应罚款金额）', max_digits=10, decimal_places=2)
  publish_amount = models.DecimalField('罚款金额', max_digits=10, decimal_places=2)
  returned = models.BooleanField('是否已还书', max_length=1, null=True, default=False, choices=((True, '是'), (False, '否')))
