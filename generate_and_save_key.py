# generate_and_save_key.py
import secrets
import os

def generate_and_save_key():
    key = secrets.token_urlsafe(32)
    
    # Create .env file if doesn't exist
    env_file = '.env'
    
    if os.path.exists(env_file):
        # Read existing .env
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Update SECRET_KEY
        with open(env_file, 'w') as f:
            key_updated = False
            for line in lines:
                if line.startswith('SECRET_KEY='):
                    f.write(f'SECRET_KEY={key}\n')
                    key_updated = True
                else:
                    f.write(line)
            
            if not key_updated:
                f.write(f'\nSECRET_KEY={key}\n')
    else:
        # Create new .env with key
        with open(env_file, 'w') as f:
            f.write(f'SECRET_KEY={key}\n')
            f.write('FLASK_DEBUG=False\n')
            f.write('FLASK_PORT=5000\n')
            f.write('ENABLE_AI_MODE=True\n')
            f.write('DEFAULT_CHAT_MODE=no_ai\n')
    
    print(f"✅ Secret key generated and saved to {env_file}")
    print(f"📋 Add this to your deployment environment:")
    print(f"SECRET_KEY={key}")
    
    return key

if __name__ == "__main__":
    generate_and_save_key()
