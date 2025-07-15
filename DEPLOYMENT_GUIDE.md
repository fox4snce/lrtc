# Deployment Guide for /lrtc Subdirectory

## Server Configuration

Your Flask app is configured to run from the `/lrtc` subdirectory. Here's how to set it up:

### 1. File Structure
Make sure your files are in the correct location on your server:
```
public_html/
└── lrtc/
    ├── app.py
    ├── wsgi.py
    ├── requirements.txt
    └── templates/
```

### 2. WSGI Configuration
The `wsgi.py` file handles the subdirectory routing. Make sure your hosting provider points to `wsgi.py` as the WSGI entry point.

### 3. PM2 Configuration
Update your PM2 configuration to use the WSGI file:

```bash
pm2 start wsgi.py --name "constitution-game" --interpreter python3
```

### 4. cPanel Configuration
In cPanel:
1. Go to "Python Apps"
2. Set the application root to `/lrtc`
3. Set the WSGI file to `wsgi.py`
4. Set the application URL to `yourdomain.com/lrtc`

### 5. .htaccess (if needed)
If you're using Apache, create a `.htaccess` file in the `lrtc` directory:

```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ wsgi.py/$1 [QSA,L]
```

### 6. Testing
After deployment, test these URLs:
- `yourdomain.com/lrtc/` - Should show the home page
- `yourdomain.com/lrtc/login` - Should show the login page
- `yourdomain.com/lrtc/challenges` - Should show challenges

### 7. Troubleshooting
If URLs are still not working:
1. Check that `wsgi.py` is being used as the entry point
2. Verify the subdirectory path matches exactly `/lrtc`
3. Restart the PM2 process: `pm2 restart constitution-game`
4. Check the PM2 logs: `pm2 logs constitution-game`

### 8. Environment Variables
Make sure these are set in your hosting environment:
- `FLASK_ENV=production`
- `PYTHONPATH=/path/to/your/app`

The app should now properly handle all URLs with the `/lrtc` prefix! 