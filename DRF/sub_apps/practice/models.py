from django.db import models


class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    # import datetime
    # create_time=models.DateTimeField(default=datetime.datetime.now)
    # now不能加括号，否则已启动项目该字段就会自动更新
    # create_time=models.DateTimeField(default=datetime.datetime.now())
    class Meta:
        # 单个字段，有索引，有唯一
        # 多个字段，有联合索引，联合唯一
        abstract = True  # 抽象表，不再数据库建立出表


class Book(BaseModel):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # db_constraint=False  逻辑上的关联，实质上没有外键联系，增删不会受外键影响，但是orm查询不影响
    publish = models.ForeignKey(to='Publish', on_delete=models.DO_NOTHING, db_constraint=False)
    # 不能写on_delete
    authors = models.ManyToManyField(to='Author', db_constraint=False)

    class Meta:
        verbose_name = '图书'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @property
    def publish_name(self):
        return self.publish.name

    def author_list(self):
        author_list = self.authors.all()
        # ll=[]
        # for author in author_list:
        #     ll.append({'name':author.name,'sex':author.get_sex_display()})
        # return ll
        return [{'name': author.name, 'sex': author.get_sex_display()} for author in author_list]


class Publish(BaseModel):
    name = models.CharField(max_length=32)
    addr = models.CharField(max_length=32)

    class Meta:
        verbose_name = '出版社'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Author(BaseModel):
    sex_choice = (
        (0, '保密'), (1, '男'), (2, '女')
    )
    name = models.CharField(max_length=32)
    sex = models.IntegerField(choices=sex_choice, default=0)
    # OneToOneField本质就是ForeignKey+unique，自己手写也可以
    author_detail = models.OneToOneField(to='AuthorDetail', db_constraint=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class AuthorDetail(BaseModel):
    mobile = models.CharField(max_length=11)

    class Meta:
        verbose_name = '作者详情'
        verbose_name_plural = verbose_name
