# 🏆 Energy Consultant Audit System

## 📋 Overview

A comprehensive audit management system for energy consultants to create, manage, and save three types of sustainability audits:

1. **Carbon Emission Audit** - Calculate facility carbon footprint
2. **IGBC Green Building Audit** - Evaluate green building certification
3. **ESG Audit** - Comprehensive sustainability and governance assessment

All audits are automatically saved to MongoDB with real-time calculations.

---

## 🎯 Features

### ✨ Common Features Across All Audits

- ✅ **Real-time Calculations** - Results update as user enters data
- ✅ **MongoDB Storage** - All audits saved with full audit trail
- ✅ **User Authentication** - JWT token required (only authenticated users can create/view audits)
- ✅ **Audit Management** - View, filter, and delete saved audits
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Statistics Dashboard** - Count of each audit type
- ✅ **Data Persistence** - All calculations and data preserved in database

---

## 🌍 1. Carbon Emission Audit

### Purpose
Calculate the carbon footprint of a facility based on energy and resource consumption.

### Parameters

| Parameter | Unit | Emission Factor | Notes |
|-----------|------|-----------------|-------|
| Electricity Consumption | kWh | 0.82 kg CO₂/kWh | India average grid |
| Natural Gas Consumption | m³ | 2.04 kg CO₂/m³ | Standard factor |
| Water Consumption | m³ | 0.34 kg CO₂/m³ | Treatment & pumping |
| Waste Generated | kg | 0.5 kg CO₂/kg | Average landfill |
| Renewable Energy % | % | Dynamic | Reduces electricity emissions |

### Calculations

```
Electricity Emissions = Electricity Consumption × 0.82
Adjusted for Renewables = Electricity Emissions × (1 - Renewable%/100)

Natural Gas Emissions = Natural Gas Consumption × 2.04

Water Emissions = Water Consumption × 0.34

Waste Emissions = Waste Generated × 0.5

Total Carbon Footprint = All emissions combined (kg CO₂)
```

### Output
- Individual emission sources (electricity, gas, water, waste)
- Renewable energy offset
- **Total Carbon Footprint (kg CO₂)**

### Database Storage
```
Collection: carbon_emission_audits
{
  user_id: ObjectId,
  facility_name: String,
  audit_period: String,
  input_data: { all parameters },
  emissions: { calculated values },
  total_carbon_footprint: Number,
  created_at: Date,
  updated_at: Date,
  status: String
}
```

---

## 🏢 2. IGBC Green Building Audit

### Purpose
Evaluate buildings against Indian Green Building Council (IGBC) certification standards.

### Categories (Max 100 Points)

| Category | Max Points | Weight | Focuses On |
|----------|-----------|--------|-----------|
| Site Selection & Planning | 10 | 10% | Location, accessibility, planning |
| Water Conservation | 10 | 10% | Water efficiency, management |
| **Energy Conservation** | **15** | **15%** | Energy efficiency, renewables, climate |
| Environment Protection | 10 | 10% | Ecology, biodiversity, habitat |
| Health & Wellbeing | 10 | 10% | Air quality, safety, occupant health |
| Construction Practices | 10 | 10% | Sustainable materials, management |
| Management & Operations | 10 | 10% | Building operations, maintenance |
| Innovation | 5 | 5% | Unique green initiatives |
| **TOTAL** | **100** | **100%** | |

### Certification Ratings

| Score Range | Rating |
|------------|--------|
| 85-100 | 🥇 **PLATINUM** |
| 70-84 | 🥈 **GOLD** |
| 55-69 | 🏅 **SILVER** |
| 40-54 | ✅ **GREEN** |
| < 40 | ❌ **NOT RATED** |

### Database Storage
```
Collection: igbc_green_building_audits
{
  user_id: ObjectId,
  building_name: String,
  audit_period: String,
  input_data: { category scores },
  scores: { calculated scores },
  total_score: Number (0-100),
  rating: String (PLATINUM/GOLD/SILVER/GREEN/NOT_RATED),
  created_at: Date,
  updated_at: Date,
  status: String
}
```

---

## 🌱 3. ESG Audit

### Purpose
Comprehensive assessment of Environmental, Social, and Governance (ESG) performance.

### Scoring Structure

Each pillar (E, S, G) scored out of 100 using weighted metrics.

#### **Environmental (E) Score**
- **Carbon Management** (30%) - Carbon reduction strategies
- **Water Management** (30%) - Water conservation efforts
- **Waste Management** (20%) - Waste reduction programs
- **Renewable Energy** (20%) - Renewable energy adoption

E_Score = (Carbon × 0.3) + (Water × 0.3) + (Waste × 0.2) + (Renewable × 0.2)

#### **Social (S) Score**
- **Employee Satisfaction** (30%) - Employee engagement levels
- **Community Impact** (30%) - Community programs and benefits
- **Health & Safety** (20%) - Workplace safety standards
- **Diversity & Inclusion** (20%) - Diversity in workforce and leadership

S_Score = (Employee × 0.3) + (Community × 0.3) + (Health & Safety × 0.2) + (Diversity × 0.2)

#### **Governance (G) Score**
- **Ethics & Compliance** (35%) - Ethical practices, compliance
- **Audit & Controls** (35%) - Internal controls, audit systems
- **Board Diversity** (15%) - Board composition and independence
- **Transparency & Reporting** (15%) - Financial and non-financial transparency

G_Score = (Ethics × 0.35) + (Audit × 0.35) + (Board × 0.15) + (Transparency × 0.15)

#### **Overall ESG Score**
```
ESG_Score = (E_Score + S_Score + G_Score) / 3
```

### ESG Rating

| ESG Score | Rating |
|-----------|--------|
| 80-100 | ⭐⭐⭐⭐⭐ **EXCELLENT** |
| 70-79 | ⭐⭐⭐⭐ **VERY GOOD** |
| 60-69 | ⭐⭐⭐ **GOOD** |
| 50-59 | ⭐⭐ **ADEQUATE** |
| < 50 | ⭐ **NEEDS IMPROVEMENT** |

### Database Storage
```
Collection: esg_audits
{
  user_id: ObjectId,
  organization_name: String,
  audit_period: String,
  input_data: { all parameters },
  scores: {
    environmental_score: Number,
    social_score: Number,
    governance_score: Number,
    esg_score: Number,
    esg_rating: String
  },
  created_at: Date,
  updated_at: Date,
  status: String
}
```

---

## 🔌 API Endpoints

### Carbon Emission Audit Endpoints

```
POST /api/audits/carbon/create
- Create new carbon audit
- Body: { facility_name, audit_period, audit_data }
- Returns: Saved audit with calculated emissions

GET /api/audits/carbon/list
- List all carbon audits for user
- Returns: Array of carbon audits

GET /api/audits/carbon/<audit_id>
- Get specific carbon audit
- Returns: Single audit details

PUT /api/audits/carbon/<audit_id>
- Update carbon audit
- Body: { audit_data }
- Returns: Updated audit

DELETE /api/audits/carbon/<audit_id>
- Delete carbon audit
- Returns: Success/failure message
```

### IGBC Green Building Audit Endpoints

```
POST /api/audits/igbc/create
- Create new IGBC audit
- Body: { building_name, audit_period, audit_data }
- Returns: Saved audit with calculated scores

GET /api/audits/igbc/list
GET /api/audits/igbc/<audit_id>
PUT /api/audits/igbc/<audit_id>
DELETE /api/audits/igbc/<audit_id>
```

### ESG Audit Endpoints

```
POST /api/audits/esg/create
- Create new ESG audit
- Body: { organization_name, audit_period, audit_data }
- Returns: Saved audit with calculated scores

GET /api/audits/esg/list
GET /api/audits/esg/<audit_id>
PUT /api/audits/esg/<audit_id>
DELETE /api/audits/esg/<audit_id>
```

---

## 📱 Frontend Pages

### 1. **audits.html** - Main Dashboard
- View all saved audits
- Filter by audit type
- Search by name/organization
- View statistics (count of each type)
- Quick links to create new audits
- Delete audits

**URL:** `http://localhost:8000/audits.html`

### 2. **carbon-audit.html** - Carbon Emission Audit Form
- Input facility name and audit period
- Enter energy/water/waste data
- Real-time emissions calculation
- Save audit to database
- View calculation breakdown

**URL:** `http://localhost:8000/carbon-audit.html`

### 3. **igbc-audit.html** - IGBC Green Building Audit Form
- Input building name and audit period
- Score 8 IGBC categories (0-100)
- Real-time score calculation
- Display IGBC rating (Platinum/Gold/Silver/Green)
- Save audit to database

**URL:** `http://localhost:8000/igbc-audit.html`

### 4. **esg-audit.html** - ESG Audit Form
- Input organization name and audit period
- Score Environmental, Social, Governance metrics
- Real-time E, S, G scores and overall ESG score
- Display ESG rating (Excellent to Needs Improvement)
- Detailed breakdown of all metrics
- Save audit to database

**URL:** `http://localhost:8000/esg-audit.html`

---

## 🚀 Quick Start

### Running the System

1. **Start Backend** (Terminal 1)
```bash
cd backend
python run.py
# Backend running on http://localhost:5000
```

2. **Start Frontend** (Terminal 2)
```bash
cd frontend/public
python -m http.server 8000
# Frontend running on http://localhost:8000
```

3. **Access the System**
```
Main Dashboard: http://localhost:8000/audits.html
Carbon Audit: http://localhost:8000/carbon-audit.html
IGBC Audit: http://localhost:8000/igbc-audit.html
ESG Audit: http://localhost:8000/esg-audit.html
```

---

## 💾 Database Collections

### carbon_emission_audits
```javascript
db.carbon_emission_audits.find()
// Shows all carbon emission audits with calculations
```

### igbc_green_building_audits
```javascript
db.igbc_green_building_audits.find()
// Shows all IGBC audits with ratings
```

### esg_audits
```javascript
db.esg_audits.find()
// Shows all ESG audits with scores
```

---

## 🔍 Example Usage

### Creating a Carbon Emission Audit

1. Navigate to `http://localhost:8000/carbon-audit.html`
2. Fill in facility information:
   - Facility Name: "Manufacturing Plant A"
   - Audit Period: "Jan 2026 - Dec 2026"
3. Enter consumption data:
   - Electricity: 50,000 kWh
   - Natural Gas: 10,000 m³
   - Water: 5,000 m³
   - Waste: 1,000 kg
   - Renewable: 20%
4. Click "Calculate Emissions"
5. Review results showing breakdown by source
6. Click "Save Audit Report" to store in MongoDB
7. View all saved audits in dashboard

### Creating an ESG Audit

1. Navigate to `http://localhost:8000/esg-audit.html`
2. Fill in organization information
3. Score each metric 0-100:
   - Environmental: Carbon (60), Water (70), Waste (65), Renewable (75)
   - Social: Employee (80), Community (75), Health (85), Diversity (70)
   - Governance: Ethics (85), Audit (80), Board (75), Transparency (80)
4. Click "Calculate ESG Score"
5. View E, S, G scores and overall ESG score
6. Click "Save Audit Report"
7. Compare against other organizations in dashboard

---

## 📊 Data Flow

```
Frontend Form
    ↓
Real-time Calculations (JavaScript)
    ↓
Display Results to User
    ↓
User clicks "Save"
    ↓
Send to Backend API (/api/audits/carbon/create, etc.)
    ↓
Backend Validates Data
    ↓
Backend Performs Server-side Calculations (verification)
    ↓
Insert into MongoDB
    ↓
Return Saved Audit to Frontend
    ↓
Display Confirmation
    ↓
Available in Dashboard
```

---

## 🔐 Security

- ✅ **JWT Authentication** - Only logged-in users can create/view audits
- ✅ **User Isolation** - Users can only see/modify their own audits
- ✅ **Input Validation** - Both frontend and backend validation
- ✅ **Database Indexes** - User ID indexed for fast queries
- ✅ **CORS Protected** - API calls restricted to frontend origin

---

## 📈 Next Enhancements

- [ ] Export audits as PDF reports
- [ ] Compare multiple audits over time
- [ ] Set reduction targets and track progress
- [ ] Generate sustainability recommendations
- [ ] Integration with real-time data sources
- [ ] Advanced analytics and trending
- [ ] Multi-user collaboration
- [ ] Audit templates and templates library
- [ ] API documentation (Swagger)
- [ ] Rate limiting on API endpoints

---

## 🧪 Testing

### Test Carbon Audit
```bash
POST http://localhost:5000/api/audits/carbon/create
Authorization: Bearer <JWT_TOKEN>
{
  "facility_name": "Test Factory",
  "audit_period": "2026-01",
  "audit_data": {
    "electricity_consumption": 50000,
    "natural_gas_consumption": 10000,
    "water_consumption": 5000,
    "waste_generated": 1000,
    "renewable_energy_percentage": 20
  }
}
```

### Test IGBC Audit
```bash
POST http://localhost:5000/api/audits/igbc/create
Authorization: Bearer <JWT_TOKEN>
{
  "building_name": "Green Office",
  "audit_period": "2026-01",
  "audit_data": {
    "site_selection": 8,
    "water_conservation": 9,
    "energy_conservation": 12,
    "environment_protection": 7,
    "health_wellbeing": 8,
    "construction_practices": 7,
    "management_operations": 8,
    "innovation": 4
  }
}
```

### Test ESG Audit
```bash
POST http://localhost:5000/api/audits/esg/create
Authorization: Bearer <JWT_TOKEN>
{
  "organization_name": "Tech Corp",
  "audit_period": "2026-01",
  "audit_data": {
    "carbon_management": 75,
    "water_management": 70,
    "waste_management": 65,
    "renewable_energy": 80,
    "employee_satisfaction": 85,
    "community_impact": 75,
    "health_safety": 88,
    "diversity_inclusion": 70,
    "ethics_compliance": 90,
    "audit_controls": 85,
    "board_diversity": 75,
    "transparency": 82
  }
}
```

---

## 📞 Support

For issues or questions, refer to:
- Backend API documentation in [backend/README.md](../backend/README.md)
- Frontend implementation in HTML files
- Backend models in [backend/app/models/](../backend/app/models/)
- Backend routes in [backend/app/routes/audits.py](../backend/app/routes/audits.py)

