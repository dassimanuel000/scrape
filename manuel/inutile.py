from datetime import datetime
import re

date = " days ago"
date = re.sub(r"\D", "", date)
print(date)

dated = datetime.today().strftime('%Y-%m')
year = datetime.today().strftime('%Y')
mois = datetime.today().strftime('%m')
day = datetime.today().strftime('%d')

print(dated)
print(mois)
print(day)


TAG_RE = re.compile(r'<[^>]+>')

text = "</p><p>Poste \u00e0 pourvoir d\u00e8s que possible<strong>, en CDI, sur notre d\u00eapot de </strong><strong>Paris 15\u00e8me</strong><strong>.</strong></p><p></p><h2>Qui sommes-nous ?</h2><p><strong>Saint-Gobain Distribution B\u00e2timent France</strong>, est le premier distributeur de mat\u00e9riaux de construction en France, au service des professionnels et de ceux "
def remove_tags(description):
    return TAG_RE.sub('', description)

description = remove_tags(text)
print(description)

if date == 30:
    date = dated
    print(date)
elif date == "Today":
    date = "{dated}" + str(date) + "T11:30:45.382Z"
    print(date)
elif date != "":
    date = day - date
    date = "{dated}" + str(date) + "T11:30:45.382Z"
    print(date)
else:
    print(date)