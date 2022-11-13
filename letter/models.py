from django.db import models


# Create your models here.
class Letter(models.Model):
    dear = models.CharField(max_length=50)
    writer = models.ForeignKey("accounts.User",
                               on_delete=models.CASCADE,
                               db_column='writer')
    content = models.CharField(max_length=255, null=True)
    is_answer = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.pk

    class Meta:
        db_table = 'letter'


class Answer(models.Model):
    letter = models.ForeignKey("letter.Letter",
                               on_delete=models.CASCADE,
                               db_column='letter')
    responser = models.ForeignKey("accounts.User",
                                  on_delete=models.CASCADE,
                                  db_column='responser')

    def __str__(self):
        return self.pk

    class Meta:
        db_table = 'answer'
