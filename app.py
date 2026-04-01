from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from config import Config
from database import db, User, CropHistory, ExpenseRecord, PestDetection
import os
import json
import base64
import pickle
import pandas as pd
import google.generativeai as genai




app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Pehle login karo!'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# ─── LOAD ML MODEL ──────────────────────────────────
try:
    with open('models/crop_model.pkl', 'rb') as f:
        crop_model = pickle.load(f)
    with open('models/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    with open('models/crop_info.pkl', 'rb') as f:
        crop_info = pickle.load(f)
    print(f"✅ ML Model loaded! Accuracy: {crop_info['accuracy']*100:.2f}%")
except Exception as e:
    print(f"⚠️ ML Model not loaded: {e}")
    crop_model     = None
    label_encoder  = None
    crop_info      = None

# ─── HOME ───────────────────────────────────────────
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# ─── REGISTER ───────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form.get('name')
        email    = request.form.get('email')
        password = request.form.get('password')
        phone    = request.form.get('phone')
        location = request.form.get('location')

        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(name=name, email=email, password=hashed_pw,
                    phone=phone, location=location)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login now.', 'success')
        return redirect(url_for('login'))
    return render_template('login.html', mode='register')

# ─── LOGIN ──────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        user     = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash(f'Welcome back, {user.name}! 🌾', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid email or password!', 'danger')
    return render_template('login.html', mode='login')

# ─── LOGOUT ─────────────────────────────────────────
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('index'))

# ─── DASHBOARD ──────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    expenses      = ExpenseRecord.query.filter_by(user_id=current_user.id).all()
    crops         = CropHistory.query.filter_by(user_id=current_user.id).order_by(
                        CropHistory.created_at.desc()).limit(5).all()
    total_expense = sum(e.amount for e in expenses)
    return render_template('dashboard.html', user=current_user,
                           expenses=expenses, crops=crops,
                           total_expense=total_expense)

# ─── WEATHER ────────────────────────────────────────
@app.route('/weather')
@login_required
def weather():
    weather_key = os.environ.get('WEATHER_API_KEY', '')
    return render_template('weather.html',
                           user=current_user,
                           weather_key=weather_key)

# ─── CROP ───────────────────────────────────────────
@app.route('/crop', methods=['GET', 'POST'])
@login_required
def crop():
    return render_template('crop.html', user=current_user)

# ─── PEST PAGE ──────────────────────────────────────
@app.route('/pest', methods=['GET', 'POST'])
@login_required
def pest():
    return render_template('pest.html', user=current_user)

# ─── CHATBOT PAGE ───────────────────────────────────
@app.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html', user=current_user)

# ─── MARKET ─────────────────────────────────────────
@app.route('/market')
@login_required
def market():
    return render_template('market.html', user=current_user)

# ─── SCHEMES ────────────────────────────────────────
@app.route('/schemes')
@login_required
def schemes():
    return render_template('schemes.html', user=current_user)

# ─── EXPENSE ────────────────────────────────────────
@app.route('/expense', methods=['GET', 'POST'])
@login_required
def expense():
    if request.method == 'POST':
        title    = request.form.get('title')
        amount   = float(request.form.get('amount'))
        category = request.form.get('category')
        record   = ExpenseRecord(user_id=current_user.id,
                                 title=title, amount=amount,
                                 category=category)
        db.session.add(record)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('expense'))
    expenses      = ExpenseRecord.query.filter_by(user_id=current_user.id).all()
    total_expense = sum(e.amount for e in expenses)
    return render_template('expense.html', user=current_user,
                           expenses=expenses,
                           total_expense=total_expense)

# ─── TIPS ───────────────────────────────────────────
@app.route('/tips')
@login_required
def tips():
    return render_template('tips.html', user=current_user)

# ─── ML CROP PREDICTION API ─────────────────────────
@app.route('/api/ml_crop', methods=['POST'])
@login_required
def api_ml_crop():
    try:
        data        = request.get_json()
        nitrogen    = float(data.get('N', 0))
        phosphorus  = float(data.get('P', 0))
        potassium   = float(data.get('K', 0))
        temperature = float(data.get('temperature', 25))
        humidity    = float(data.get('humidity', 60))
        ph          = float(data.get('ph', 6.5))
        rainfall    = float(data.get('rainfall', 100))

        if crop_model is None:
            return jsonify({'error': 'ML Model not loaded!'}), 500

        input_data = pd.DataFrame(
            [[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]],
            columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        )

        prediction    = crop_model.predict(input_data)
        crop_name     = label_encoder.inverse_transform(prediction)[0]
        probabilities = crop_model.predict_proba(input_data)[0]
        top3_idx      = probabilities.argsort()[-3:][::-1]
        top3_crops    = [
            {
                'crop':       label_encoder.classes_[i],
                'confidence': round(float(probabilities[i]) * 100, 1)
            }
            for i in top3_idx
        ]

        fertilizer_map = {
            'rice':        'N:120kg/ha, P:60kg/ha, K:60kg/ha — Urea + DAP combination',
            'wheat':       'N:150kg/ha, P:60kg/ha, K:40kg/ha — DAP + MOP as basal dose',
            'maize':       'N:120kg/ha, P:60kg/ha, K:40kg/ha — Apply in 3 split doses',
            'cotton':      'N:120kg/ha, P:60kg/ha, K:60kg/ha — Apply in split doses',
            'sugarcane':   'N:250kg/ha, P:85kg/ha, K:60kg/ha — Apply in 4 split doses',
            'chickpea':    'P:60kg/ha, K:20kg/ha — Rhizobium seed inoculation',
            'kidneybeans': 'P:60kg/ha, K:40kg/ha — Rhizobium seed treatment',
            'pigeonpeas':  'P:50kg/ha, K:30kg/ha — Rhizobium seed treatment',
            'mothbeans':   'N:20kg/ha, P:40kg/ha — Minimal fertilizer needed',
            'mungbean':    'P:40kg/ha, K:20kg/ha — Rhizobium inoculation',
            'blackgram':   'P:40kg/ha, K:20kg/ha — Rhizobium seed treatment',
            'lentil':      'P:40kg/ha, K:20kg/ha — Seed inoculation recommended',
            'pomegranate': 'N:625g, P:250g, K:200g per plant per year',
            'banana':      'N:200g, P:60g, K:300g per plant',
            'mango':       'N:500g, P:200g, K:400g per tree per year',
            'grapes':      'N:90kg/ha, P:60kg/ha, K:90kg/ha',
            'watermelon':  'N:80kg/ha, P:40kg/ha, K:60kg/ha — Drip irrigation',
            'muskmelon':   'N:80kg/ha, P:40kg/ha, K:60kg/ha',
            'apple':       'N:70g, P:35g, K:70g per tree',
            'orange':      'N:400g, P:200g, K:400g per tree per year',
            'papaya':      'N:250g, P:250g, K:500g per plant per year',
            'coconut':     'N:500g, P:320g, K:1200g per palm per year',
            'jute':        'N:60kg/ha, P:30kg/ha, K:30kg/ha',
            'coffee':      'N:30g, P:15g, K:30g per plant',
        }

        fertilizer = fertilizer_map.get(
            crop_name.lower(),
            'Consult local agriculture department for specific doses'
        )

        # Save to database
        record = CropHistory(
            user_id   = current_user.id,
            crop_name = crop_name,
            soil_type = f"N:{nitrogen} P:{phosphorus} K:{potassium}",
            season    = f"pH:{ph} Temp:{temperature}°C",
        )
        db.session.add(record)
        db.session.commit()

        return jsonify({
            'status':     'ok',
            'crop':       crop_name,
            'confidence': round(float(probabilities.max()) * 100, 1),
            'top3':       top3_crops,
            'fertilizer': fertilizer,
            'accuracy':   round(float(crop_info['accuracy']) * 100, 2),
        })

    except Exception as e:
        print(f"ML ERROR: {e}")
        return jsonify({'error': str(e)}), 500

# ─── CHAT API ───────────────────────────────────────
@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    data    = request.get_json()
    message = data.get('message', '')

    try:
        gemini_key = os.environ.get('GEMINI_API_KEY', '')
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""You are CropSense AI — an expert Indian farming assistant.

Farmer's message: "{message}"

MOST IMPORTANT RULE — LANGUAGE DETECTION:
- Detect what language the farmer used in their message
- Reply in EXACTLY that same language
- If they wrote in Hindi → reply in Hindi
- If they wrote in English → reply in English
- If they wrote in Hinglish (Hindi+English mix) → reply in Hinglish
- If they wrote in Marathi → reply in Marathi
- If they wrote in Punjabi → reply in Punjabi
- If they wrote in Gujarati → reply in Gujarati
- If they wrote in Telugu → reply in Telugu
- If they wrote in Tamil → reply in Tamil
- If they wrote in Bengali → reply in Bengali
- If they wrote in Kannada → reply in Kannada
- Match their exact style — casual or formal.

FARMING RULES:
- Give practical, accurate farming advice
- Use relevant emojis
- Maximum 200 words
- Indian farming context only
- Real crop names, fertilizer doses, government schemes"""

        response = model.generate_content(prompt)
        return jsonify({'reply': response.text, 'status': 'ok'})

    except Exception as e:
        print(f"CHAT ERROR: {e}")
        return jsonify({'reply': f'❌ Error: {str(e)}', 'status': 'error'})

# ─── PEST DETECTION API ─────────────────────────────
@app.route('/api/detect_pest', methods=['POST'])
@login_required
def api_detect_pest():
    if 'image' not in request.files:
        return jsonify({'error': 'No image'}), 400

    file      = request.files['image']
    crop_type = request.form.get('crop_type', 'unknown crop')

    try:
        gemini_key = os.environ.get('GEMINI_API_KEY', '')
        genai.configure(api_key=gemini_key)
       model = genai.GenerativeModel('gemini-pro')

        img_bytes = file.read()
        img_b64   = base64.b64encode(img_bytes).decode()

        prompt = f"""You are an expert agricultural disease and pest detection AI.
Analyze this plant image (crop type: {crop_type}).

Respond ONLY in this exact JSON format (no markdown, no extra text):
{{
  "name": "Disease name in Hindi and English",
  "icon": "relevant emoji",
  "severity": "high/medium/low",
  "description": "2-3 line description in Hindi",
  "treatment": "<p>• Treatment step 1</p><p>• Treatment step 2</p><p>• Treatment step 3</p>",
  "prevention": "<p>• Prevention tip 1</p><p>• Prevention tip 2</p><p>• Prevention tip 3</p>"
}}"""

        response = model.generate_content([
            prompt,
            {'mime_type': file.content_type or 'image/jpeg', 'data': img_b64}
        ])

        text = response.text.strip()
        if '```' in text:
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]

        result = json.loads(text.strip())

        pest_record = PestDetection(
            user_id    = current_user.id,
            image_path = file.filename,
            result     = str(result.get('name', ''))
        )
        db.session.add(pest_record)
        db.session.commit()

        return jsonify(result)

    except Exception as e:
        print(f"PEST ERROR: {e}")
        return jsonify({
            'name':        'Detection Failed',
            'icon':        '❌',
            'severity':    'medium',
            'description': 'Image analyze nahi ho saki. Dobara try karo.',
            'treatment':   '<p>• Clear photo lo</p><p>• Leaf close-up do</p>',
            'prevention':  '<p>• Dobara try karo</p>'
        })

    if __name__ == "__main__":
       app.run(host="0.0.0.0", port=7860)

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=7860)
