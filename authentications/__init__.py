from authentications.bearer import auth

# Set alias for auth.login_required. Why not, it's stupid name.
setattr(auth, 'bearer_token', auth.login_required)

# Authentication example for a route.
# @app.route('/auth/test')
# @auth.token <-- !Auth decorator for secret routes!
# def secret_route():
#     return jsonify({'message': 'You may enter'})