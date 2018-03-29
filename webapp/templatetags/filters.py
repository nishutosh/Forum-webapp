from django import template
register = template.Library()

@register.filter
def viewscut(value):
   if value>1000:
   	  value=value/1000
   	  return str(value)+"k"
   elif value>100000:
   	  value=value/100000
   	  return str(value)+"l"
   else:
      return value	  