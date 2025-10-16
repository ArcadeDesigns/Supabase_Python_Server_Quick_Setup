# package/__init__.py
import os
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_login import UserMixin
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from supabase import create_client, Client
from package.authentication import Authentication
from package.security import Security

# ==============================
# 1️⃣ Load Environment Variables
# ==============================
load_dotenv()


# ==============================
# 2️⃣ Initialize Flask App
# ==============================
app = Flask(__name__, template_folder="../templates",
            static_folder="../static")
csrf = CSRFProtect(app)

# Configure CORS based on environment
if os.getenv('APPLICATION_ENVIRONMENT') == 'PRODUCTION':
    # Production: only allow specific origins
    allowed_origins = [
        'https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxx.com'
    ]
    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "x-api-key", "x-signature", "X-CSRFToken"]
        }
    })
else:
    # Development: allow all origins with CSRF support
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "x-api-key", "x-signature", "X-CSRFToken"]
        }
    })

# ==============================
# 3️⃣ Configuration
# ==============================
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DEBUG"] = os.getenv(
    "APPLICATION_ENVIRONMENT", "").upper() == "DEVELOPMENT"


# ==============================
# 4️⃣ Logging Setup
# ==============================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==============================
# 5️⃣ Flask Login Setup
# ==============================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# ==============================
# 6️⃣ Third-Party Integrations
# ==============================
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_API")

# Google OAuth
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv(
    "GOOGLE_REDIRECT_URI", "https://xxxxxxxxxx.xxxxxxxxxx/auth/callback/redirect")

GOOGLE_AUTH_URL = "https://accounts.google.xxxxxxxxxx/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://accounts.google.xxxxxxxxxx/o/oauth2/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.xxxxxxxxxx/oauth2/v1/userinfo"


# ==============================
# 7️⃣ Supabase Setup
# ==============================
SUPABASE_URL = os.getenv("APPLICATION_DATABASE")
SUPABASE_KEY = os.getenv("APPLICATION_DATABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ==============================
# 8️⃣ Authentication Initialization
# ==============================
authentication = Authentication(supabase)
