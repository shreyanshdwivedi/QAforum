from django.contrib import admin
from .models import User, Question, Answer, Comment, UpVoteQues, DownVoteQues, UpVoteAns, DownVoteAns

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(UpVoteQues)
admin.site.register(DownVoteQues)
admin.site.register(UpVoteAns)
admin.site.register(DownVoteAns)

