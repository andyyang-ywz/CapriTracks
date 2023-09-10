from datetime import date, timedelta

def get_current_monday_date(request):
   return {'monday_date': (date.today() - timedelta(days=date.today().weekday())).strftime('%Y-%m-%d')}
