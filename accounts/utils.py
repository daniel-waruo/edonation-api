from .models import User


def create_knox_token(token_model, user, serializer):
    instance, token = token_model.objects.create(user=user)
    return token


def generate_username(full_name):
    name = full_name.lower()
    name = name.split(' ')
    last_name = name[-1]
    first_name = name[0]
    # try initials first names plus last whole name
    username = '{}{}'.format(first_name[0], last_name)
    if User.objects.filter(username=username).count() > 0:
        # if not, try first full name plus initials from last names
        username = '{}{}'.format(first_name, last_name[0])
        if User.objects.filter(username=username).count() > 0:
            # if it doesn't fit, put the first name plus a number
            users = User.objects.filter(username__regex=r'^%s[1-9]{1,}$' % first_name).order_by('username').values(
                'username')
            if len(users) > 0:
                last_number_used = list(map(lambda x: int(x['username'].replace(first_name, '')), users))
                last_number_used.sort()
                last_number_used = last_number_used[-1]
                number = last_number_used + 1
                username = '{}{}'.format(first_name, number)
            else:
                username = '{}{}'.format(first_name, 1)
    return username
