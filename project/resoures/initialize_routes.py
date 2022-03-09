from .movies import MovieApi, MoviesApi
from .auth import Signup, LoginApi
from ..services.reset_password import ForgetPassword, ResetPassword

def initialize_routes(api):
    api.add_resource(MovieApi, '/api/movies/<id>')
    api.add_resource(MoviesApi, '/api/movies')
    api.add_resource(Signup, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
    api.add_resource(ForgetPassword, '/api/auth/forgot')
    api.add_resource(ResetPassword, '/api/auth/reset')
