# 🌾 CropSense AI — Smart Farming Assistant

> An AI-powered personal farming assistant built for Indian farmers using Python, Flask, Scikit-learn, and Gemini AI.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![ML Accuracy](https://img.shields.io/badge/ML%20Accuracy-99.55%25-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Project Info

| Detail | Info |
|--------|------|
| **Project Name** | CropSense AI — Smart Farming Assistant |
| **University** | JSPM University, Pune |
| **Department** | School of Computational Sciences |




---

## 📖 About the Project

**CropSense AI** is an intelligent web-based farming assistant that helps Indian farmers make better agricultural decisions using Artificial Intelligence and Machine Learning.

The system provides:
- 🌱 **AI-powered crop recommendations** based on soil NPK values, pH, temperature, humidity and rainfall
- 🐛 **Plant disease detection** using image analysis (Gemini Vision AI)
- 🤖 **Multilingual AI chatbot** supporting 10 Indian languages
- 📊 **Real-time market prices** for 35+ commodities
- 🌤️ **Weather forecasting** with farming-specific advice
- 🏛️ **Government scheme information** with direct apply links
- 💰 **Farm expense tracking** with category-wise analytics
- 💡 **Expert farming tips** across 7 categories

---

## 🚀 Features

### 🧪 ML-Powered Crop Recommendation
- Trained on **Kaggle Crop Recommendation Dataset** (2200 samples, 22 crops)
- **Random Forest Classifier** — 99.55% accuracy
- Input: N, P, K, Temperature, Humidity, pH, Rainfall
- Output: Top 3 crop recommendations with confidence scores

### 🐛 Pest & Disease Detection
- Upload plant leaf photo
- **Gemini Vision AI** analyzes and identifies disease
- Provides severity level, treatment plan, and prevention tips

### 🤖 AI Chatbot
- Powered by **Google Gemini 2.5 Flash**
- Auto-detects language — replies in same language
- Supports: Hindi, English, Hinglish, Marathi, Punjabi, Gujarati, Telugu, Tamil, Bengali, Kannada
- Voice input support

### 🌤️ Weather Dashboard
- Real-time weather data via **OpenWeatherMap API**
- 5-day forecast
- AI-generated farming advice based on current weather

### 📊 Live Market Prices
- 35+ commodities with daily price updates
- Filter by category (Grains, Vegetables, Fruits, Pulses, Spices)
- Filter by state

### 🏛️ Government Schemes
- 12 real government schemes
- PM Kisan Samman Nidhi, Fasal Bima, KCC, KUSUM Solar Pump, and more
- Direct apply links

### 💰 Expense Tracker
- Track farm expenses by category
- Category-wise breakdown with progress bars
- Average expense calculation

---

## 🛠️ Technology Stack

### Backend
| Technology | Purpose |
|-----------|---------|
| Python 3.10 | Primary programming language |
| Flask 3.0 | Web framework |
| Flask-Login | User authentication |
| Flask-SQLAlchemy | Database ORM |
| Flask-Bcrypt | Password hashing |

### Machine Learning
| Library | Purpose |
|---------|---------|
| Scikit-learn | Random Forest ML model |
| Pandas | Data processing |
| NumPy | Numerical computing |
| Pickle | Model serialization |

### AI & APIs
| Service | Purpose |
|---------|---------|
| Google Gemini 2.5 Flash | Chatbot + Pest Detection |
| OpenWeatherMap API | Real-time weather data |

### Frontend
| Technology | Purpose |
|-----------|---------|
| HTML5 | Structure |
| CSS3 + Inter Font | Styling |
| JavaScript (ES6+) | Interactivity |

### Database
| Technology | Purpose |
|-----------|---------|
| SQLite | User data, expenses, history |

---

## 📁 Project Structure
```
ai_farming_assistant/
│
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── database.py             # Database models
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not in repo)
│
├── models/
│   ├── train_model.py      # ML model training script
│   ├── crop_model.pkl      # Trained Random Forest model
│   ├── label_encoder.pkl   # Label encoder
│   ├── crop_info.pkl       # Model metadata
│   └── Crop_recommendation.csv  # Kaggle dataset
│
├── templates/
│   ├── base.html           # Base template
│   ├── index.html          # Landing page
│   ├── login.html          # Login/Register
│   ├── dashboard.html      # Main dashboard
│   ├── crop.html           # Crop recommendation
│   ├── pest.html           # Pest detection
│   ├── chatbot.html        # AI chatbot
│   ├── weather.html        # Weather forecast
│   ├── market.html         # Market prices
│   ├── schemes.html        # Govt schemes
│   ├── expense.html        # Expense tracker
│   └── tips.html           # Farming tips
│
├── static/
│   ├── css/style.css       # Main stylesheet
│   └── js/main.js          # Main JavaScript
│
├── database/
│   └── farming.db          # SQLite database
│
└── uploads/                # Pest detection image uploads
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Step 1 — Clone the Repository
```bash
git clone https://github.com/yourusername/cropsense-ai.git
cd cropsense-ai
```

### Step 2 — Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate


```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Configure API Keys
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
WEATHER_API_KEY=your-openweathermap-api-key
GEMINI_API_KEY=your-google-gemini-api-key
```

**Get API Keys:**
- OpenWeatherMap: https://openweathermap.org/api (Free)
- Google Gemini: https://aistudio.google.com (Free)







### Step 5 — Train ML Model
```bash
cd models
python train_model.py
cd ..
```

### Step 6 — Run the Application
```bash
python app.py
```

Open browser: **http://127.0.0.1:5000**

---

## 🗄️ Database Schema

### User Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| name | String | Full name |
| email | String | Unique email |
| password | String | Hashed password |
| phone | String | Phone number |
| location | String | City/Village |

### CropHistory Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key |
| crop_name | String | Predicted crop |
| soil_type | String | Soil/NPK data |
| season | String | Season/Climate |

### ExpenseRecord Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key |
| title | String | Expense name |
| amount | Float | Amount in ₹ |
| category | String | Expense category |

---

## 🤖 ML Model Details

| Detail | Value |
|--------|-------|
| **Algorithm** | Random Forest Classifier |
| **Dataset** | Kaggle Crop Recommendation Dataset |
| **Training Samples** | 1760 (80%) |
| **Testing Samples** | 440 (20%) |
| **Total Samples** | 2200 |
| **Number of Crops** | 22 |
| **Accuracy** | 99.55% |
| **Features** | N, P, K, Temperature, Humidity, pH, Rainfall |

### Supported Crops
Rice, Wheat, Maize, Cotton, Sugarcane, Chickpea, Kidney Beans,
Pigeon Peas, Moth Beans, Mung Bean, Black Gram, Lentil,
Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon,
Apple, Orange, Papaya, Coconut, Jute, Coffee

---

## 📸 Screenshots

| Page | Description |
|------|-------------|
| Homepage | Modern landing page with farmer illustration |
| Login/Register | Split-screen authentication |
| Dashboard | Stats, quick access, profit calculator |
| Crop Recommendation | ML Model + Simple mode |
| Pest Detection | AI image analysis |
| AI Chatbot | Multilingual chat interface |
| Weather | Real-time forecast dashboard |
| Market Prices | Live commodity prices with ticker |
| Govt Schemes | 12 schemes with apply links |
| Expense Tracker | Category-wise expense analytics |

---

## 🔮 Future Scope

- [ ] Mobile app (React Native / Flutter)
- [ ] IoT sensor integration (soil moisture, temperature)
- [ ] Satellite imagery for crop health monitoring
- [ ] Price prediction using time-series ML
- [ ] Community forum for farmers
- [ ] Offline mode support
- [ ] SMS alerts for weather warnings
- [ ] Integration with e-commerce for selling crops

---

## 📚 References

1. Kamilaris & Prenafeta-Boldú — *Deep Learning in Agriculture* (2018)
2. Shankar et al. — *Crop Yield Prediction using ML* (2019)
3. Wolfert et al. — *Big Data in Smart Farming* (2017)
4. Mohanty et al. — *Plant Disease Detection using Deep Learning* (2016)
5. Kaggle — *Crop Recommendation Dataset* by Atharva Ingle

---

## 📄 License

This project is developed for academic purposes at JSPM University, Pune.

---

<div align="center">
  <strong>🌾 CropSense AI — Empowering Indian Farmers with Technology 🌾</strong>
  <br/>
  Made with 💚 by Team CropSense AI — JSPM University, Pune
</div>