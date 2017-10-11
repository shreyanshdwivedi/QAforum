from django import template

register = template.Library()

@register.simple_tag
def get_upvoted_answer(ques, upvotedAns):

