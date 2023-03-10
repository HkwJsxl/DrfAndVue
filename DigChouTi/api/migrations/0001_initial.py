# Generated by Django 3.2.16 on 2022-12-31 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, verbose_name='内容')),
                ('depth', models.IntegerField(default=0, verbose_name='深度')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('descendant_update_datetime', models.DateTimeField(auto_now_add=True, verbose_name='后代更新时间')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False, verbose_name='已删除')),
                ('zone', models.IntegerField(choices=[(1, '42区'), (2, '段子'), (3, '图片'), (4, '挨踢1024'), (5, '你问我答')], verbose_name='专区')),
                ('title', models.CharField(max_length=150, verbose_name='文字')),
                ('url', models.CharField(blank=True, max_length=200, null=True, verbose_name='链接')),
                ('image', models.TextField(blank=True, help_text='逗号分割', null=True, verbose_name='图片地址')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.IntegerField(choices=[(1, '待审核'), (2, '已通过'), (3, '未通过')], default=1, verbose_name='状态')),
                ('collect_count', models.IntegerField(default=0, verbose_name='收藏数')),
                ('recommend_count', models.IntegerField(default=0, verbose_name='推荐数')),
                ('comment_count', models.IntegerField(default=0, verbose_name='评论数')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False, verbose_name='已删除')),
                ('title', models.CharField(db_index=True, max_length=16, verbose_name='话题')),
                ('is_hot', models.BooleanField(default=False, verbose_name='热门话题')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False, verbose_name='已删除')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('phone', models.CharField(db_index=True, max_length=32, verbose_name='手机号')),
                ('password', models.CharField(max_length=18, verbose_name='密码')),
                ('token', models.CharField(blank=True, db_index=True, max_length=64, null=True, verbose_name='token')),
                ('token_expiry_date', models.DateTimeField(blank=True, null=True, verbose_name='token有效期')),
                ('status', models.IntegerField(choices=[(1, '激活'), (2, '禁用')], default=1, verbose_name='状态')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.AddIndex(
            model_name='userinfo',
            index=models.Index(fields=['username', 'password'], name='idx_name_pwd'),
        ),
        migrations.AddField(
            model_name='topic',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userinfo', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='recommend',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.news', verbose_name='资讯'),
        ),
        migrations.AddField(
            model_name='recommend',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userinfo', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='news',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.topic', verbose_name='话题'),
        ),
        migrations.AddField(
            model_name='news',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userinfo', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='comment',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.news', verbose_name='资讯'),
        ),
        migrations.AddField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_list', to='api.comment', verbose_name='回复'),
        ),
        migrations.AddField(
            model_name='comment',
            name='root',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='descendant', to='api.comment', verbose_name='根评论'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userinfo', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='collect',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.news', verbose_name='资讯'),
        ),
        migrations.AddField(
            model_name='collect',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userinfo', verbose_name='用户'),
        ),
        migrations.AddConstraint(
            model_name='recommend',
            constraint=models.UniqueConstraint(fields=('news', 'user'), name='uni_recommend_news_user'),
        ),
        migrations.AddConstraint(
            model_name='collect',
            constraint=models.UniqueConstraint(fields=('news', 'user'), name='uni_collect_news_user'),
        ),
    ]
