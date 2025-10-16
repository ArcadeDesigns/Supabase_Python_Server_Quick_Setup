class Authentication:
    def __init__(self, supabase):
        self.supabase = supabase

    # ==============================
    # 🔟 User Sign up Function
    # ==============================

    def sign_up(self, payload):
        email = payload.get('EmailAddress')
        password = payload.get('UserPassword')
        try:
            response = self.supabase.auth.sign_up(
                {'email': email, 'password': password})
            if response.user:
                return {"status": "success", "user": response.user.email}
            return {"status": "error", "message": "Signup failed."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ==============================
    # 🔟 User Login Function
    # ==============================

    def sign_in(self, payload):
        email = payload.get('EmailAddress')
        password = payload.get('UserPassword')
        try:
            response = self.supabase.auth.sign_in_with_password(
                {'email': email, 'password': password})
            return {"status": "success", "session": response.session, "user": response.user.email}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ==============================
    # 🔟 User Sign Out Function
    # ==============================

    def sign_out(self):
        try:
            self.supabase.auth.sign_out()
            return {"status": "success", "message": "User signed out successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
