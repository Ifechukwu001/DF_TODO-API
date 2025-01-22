from dj_rest_auth.serializers import LoginSerializer as DJLoginSerializer


class LoginSerializer(DJLoginSerializer):
    email = None
