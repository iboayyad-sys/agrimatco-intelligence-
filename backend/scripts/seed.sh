#!/usr/bin/env bash
set -e

echo "Seeding database with sample data..."

python -c "
import os
os.environ.setdefault('DATABASE_URL', os.getenv('DATABASE_URL', 'postgresql://agrimatco:agrimatco_password@localhost:5432/agrimatco_db'))

from app.database import SessionLocal
from app.models import Crop, Disease, GrowthStage, Product

db = SessionLocal()

# Check if data already exists
if db.query(Crop).first():
    print('Database already seeded')
    db.close()
    exit(0)

# Add sample crops
crops_data = [
    {'name': 'Wheat', 'name_ar': 'القمح', 'scientific_name': 'Triticum aestivum'},
    {'name': 'Tomato', 'name_ar': 'الطماطم', 'scientific_name': 'Solanum lycopersicum'},
    {'name': 'Potato', 'name_ar': 'البطاطا', 'scientific_name': 'Solanum tuberosum'},
    {'name': 'Corn', 'name_ar': 'الذرة', 'scientific_name': 'Zea mays'},
]

crops = []
for crop_data in crops_data:
    crop = Crop(**crop_data)
    db.add(crop)
    crops.append(crop)

db.commit()

# Add sample diseases
diseases_data = [
    {
        'crop_id': crops[0].id,
        'name': 'Powdery Mildew',
        'name_ar': 'البياض الدقيقي',
        'description': 'Fungal disease causing white powder on leaves',
        'symptoms': ['white powder on leaves', 'leaf curling'],
        'causes': ['high humidity', 'poor air circulation'],
        'severity_level': 'Medium',
    },
    {
        'crop_id': crops[1].id,
        'name': 'Early Blight',
        'name_ar': 'اللفحة المبكرة',
        'description': 'Fungal disease affecting tomato leaves',
        'symptoms': ['brown spots', 'concentric rings'],
        'causes': ['wet conditions', 'fungal spores'],
        'severity_level': 'High',
    },
]

for disease_data in diseases_data:
    disease = Disease(**disease_data)
    db.add(disease)

db.commit()

# Add sample products
products_data = [
    {
        'name': 'Fungicide Pro',
        'name_ar': 'مبيد الفطريات برو',
        'category': 'Fungicide',
        'description': 'Broad spectrum fungicide',
        'active_ingredient': 'Mancozeb',
        'concentration': '80% WP',
        'dosage': '2-3 g/L',
        'safety_info': 'Wear protective equipment',
        'pre_harvest_interval': 7,
        'price': 25.50,
    },
    {
        'name': 'Insect Shield',
        'name_ar': 'درع الحشرات',
        'category': 'Insecticide',
        'description': 'Effective against common pests',
        'active_ingredient': 'Cypermethrin',
        'concentration': '10% EC',
        'dosage': '1-2 ml/L',
        'safety_info': 'Keep away from children',
        'pre_harvest_interval': 14,
        'price': 18.75,
    },
]

for product_data in products_data:
    product = Product(**product_data)
    db.add(product)

db.commit()
print('Database seeded successfully with sample data')
db.close()
"
