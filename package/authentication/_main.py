class Authentication:
    def __init__(self, supabase):
        self.supabase = supabase

    # ==============================
    # 🔟 User Sign up Function
    # ==============================

    def sign_up(self, payload):
        try:
            email = payload.get("email")
            password = payload.get("password")
            full_name = payload.get("full_name")

            if not email or not password:
                return {
                    "status": "error",
                    "message": "You must provide both an email and password."
                }

            # ✅ Create user in Supabase Auth
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name
                    }
                }
            })

            if response.user is None:
                return {
                    "status": "error",
                    "message": "Failed to create account. Please try again."
                }

            return {
                "status": "success",
                "message": "Account created successfully.",
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                    "full_name": full_name
                }
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    # ==============================
    # 🔟 User Login Function
    # ==============================

    def sign_in(self, payload):
        email = payload.get("email")
        password = payload.get("password")

        if not email or not password:
            return {"status": "error", "message": "Email and password are required."}

        try:
            response = self.supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )

            if response.user is None:
                return {"status": "error", "message": "Invalid login credentials."}

            return {
                "status": "success",
                "session": {
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                    "expires_at": response.session.expires_at,
                },
                "user": {
                    "id": response.user.id,
                    "email": response.user.email
                },
            }

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
