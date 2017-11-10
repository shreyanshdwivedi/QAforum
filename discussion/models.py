from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    bio = models.CharField(max_length=500, null=True)
    image = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.username

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, unique=False)
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    reward = models.IntegerField(default=0)
    closed = models.BooleanField(default=False)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    answers = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    updated = models.DateTimeField('date updated', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    answer = models.BooleanField(default=False)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.answer_text

    class Meta:
        ordering = ['-answer', '-pub_date']

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    updated = models.DateTimeField('date updated', auto_now=True)
    def __str__(self):
        return self.comment

class UpVoteQues(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    upvote_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

class DownVoteQues(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    downvote_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

class AddStar(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    star_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class UpVoteAns(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    upvote_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user

class DownVoteAns(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    downvote_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user
