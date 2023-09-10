from django import template
import json, calendar

register = template.Library()

class Flash_Mess:
   def __init__(self, title=None, content=None, date=None):
      self.title = title
      self.content = content
      self.date = date

@register.filter(name="jsonify")
def jsonify(data):
   data = str(data)
   result = json.loads(data)

   if 'title' in result:
      flash_mess = Flash_Mess(result['title'], result['content'])
   else:
      flash_mess = Flash_Mess(date=result['date'])

   return flash_mess

@register.filter(name="get_day_name")
def get_day_name(day_num):
   return calendar.day_name[day_num]


@register.filter(name="total_time")
def total_time(tracks):
   minutes = 0
   for track in tracks:
      minutes += int(track.time)

   return f"{minutes // 60} hour(s) {minutes % 60} minute(s)"
