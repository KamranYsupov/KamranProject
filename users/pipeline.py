import requests
from django.contrib.auth.models import Group


def auth_user_form_social(backend, user, *args, **kwargs):
    response = None
    oauth_group = Group.objects.get(name='oauth')
    github_avatar_url = 'https://avatars.githubusercontent.com/'

    if str(backend).__contains__('GithubOAuth2'):
        response = requests.get(github_avatar_url + str(user.username))

    if response:
        with open(f'media/users/oauth_avatars/{user.username}.png', 'wb') as file:
            file.write(response.content)
            user.avatar = f'users/oauth_avatars/{user.username}.png'
            user.save()

    user.groups.add(oauth_group)
