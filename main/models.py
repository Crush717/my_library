from django.db import models


class ReaderType(models.Model):
    """
    读者类别
    """
    name = models.CharField("名称", max_length=255)
    can_borrow_book_num = models.IntegerField("可借书数量")
    can_borrow_days = models.IntegerField("可借书天数")
    can_renew_times = models.IntegerField("可续借次数")
    punish_rate = models.DecimalField("罚款率（元/天）", max_digits=4, decimal_places=2,
                                      help_text="超过可借书天数后，每本每天多少钱")
    valid_year = models.IntegerField("有效期（年）", help_text="0 为永久有效")


class Reader(models.Model):
    """
    读者
    """
    no = models.CharField(max_length=255)
    name = models.CharField(max_length=255,
                            # 不能为空
                            blank=False)
    sex = models.CharField(max_length=1, null=True, choices=(
        (1, "男"),
        (2, "女")
    ))
    reader_type = models.ForeignKey(ReaderType,
                                    # 删除关联表规则
                                    on_delete=models.DO_NOTHING,
                                    # 虚拟外键，表中实际上不会创建外键
                                    db_constraint=True,
                                    null=True
                                    )
    phone_number = models.CharField(max_length=11, null=True)

    # TODO ……


class Book(models.Model):
    """
    图书信息
    """
    code = models.CharField("书号", max_length=255)
    name = models.CharField("书名", max_length=255)
    authors = models.CharField("作者", max_length=255)
    publisher = models.CharField("出版社", max_length=255)
    publish_time = models.DateTimeField("出版日期")
    isbn = models.CharField("ISBN", max_length=255)
    catalog = models.CharField("分类号", max_length=255)
    language = models.CharField("语言", max_length=2, null=True, choices=(
        (1, "中文"), (2, "英文"), (3, "日文"),
        (4, "俄文"), (5, "德文"), (6, "法文"),
        (99, "其他")
    ))
    total_pages = models.IntegerField("总页数")
    price = models.DecimalField("价格", max_digits=10, decimal_places=2)


class BorrowRecord(models.Model):
    """
    借阅信息
    """
    reader_id = models.BigIntegerField("读者ID")
    book_id = models.BigIntegerField("图书ID")
    renew_times = models.IntegerField("续借次数")
    created_times = models.DateTimeField("创建时间/借书时间")
    plan_return_time = models.DateTimeField("应还时间")
    return_time = models.DateTimeField("实际还书时间")
    overdue_days = models.IntegerField("超期天数")
    overdue_amount = models.DecimalField("超期金额（应罚款金额）", max_digits=10, decimal_places=2)
    publish_amount = models.DecimalField("罚款金额", max_digits=10, decimal_places=2)
    returned = models.CharField("是否已还书", max_length=1, null=True, choices=(
             (1, "是"), (2, "否")
    ))
