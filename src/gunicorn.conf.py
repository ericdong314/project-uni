bind = [':8888']
wsgi_app = 'uni.wsgi:application'
accesslog = '-'
# access_log_format = ('Host: %({host}i)s X-Forwarded-For: %({x-forwarded-for}i)s '
#                      'X-Forwarded-Proto: %({x-forwarded-proto}i)s '
#                      'Origin: %({origin}i)s '
#                      'Referer: %({referer}i)s ')