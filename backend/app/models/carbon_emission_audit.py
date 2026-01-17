from datetime import datetime
from bson import ObjectId
from app.db.mongo import MongoDB


class CarbonEmissionAudit:
    """Model for Carbon Emission Audit"""
    
    COLLECTION_NAME = 'carbon_emission_audits'
    
    @staticmethod
    def _get_collection():
        """Get MongoDB collection"""
        return MongoDB.get_collection(CarbonEmissionAudit.COLLECTION_NAME)
    
    @staticmethod
    def create_indexes():
        """Create database indexes"""
        collection = CarbonEmissionAudit._get_collection()
        collection.create_index("user_id")
        collection.create_index("created_at")
        collection.create_index("facility_name")
    
    @staticmethod
    def create_audit(user_id, facility_name, audit_period, data):
        """Create a new carbon emission audit
        
        Args:
            user_id: User ID (ObjectId)
            facility_name: Name of facility being audited
            audit_period: Period of audit (e.g., "Jan 2026 - Dec 2026")
            data: Dictionary containing:
                - electricity_consumption (kWh)
                - natural_gas_consumption (m3)
                - water_consumption (m3)
                - waste_generated (kg)
                - renewable_energy_percentage (%)
        
        Returns:
            Inserted audit ID
        """
        # Calculate emissions
        emissions = CarbonEmissionAudit.calculate_emissions(data)
        
        audit_doc = {
            'user_id': ObjectId(user_id),
            'facility_name': facility_name,
            'audit_period': audit_period,
            'input_data': data,
            'emissions': emissions,
            'total_carbon_footprint': emissions['total_carbon_footprint'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'status': 'completed'
        }
        
        collection = CarbonEmissionAudit._get_collection()
        result = collection.insert_one(audit_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def calculate_emissions(data):
        """Calculate carbon emissions based on input data
        
        Emission factors (kg CO2):
        - Electricity: 0.82 kg CO2/kWh (India average grid)
        - Natural Gas: 2.04 kg CO2/m3
        - Water: 0.34 kg CO2/m3
        - Waste: 0.5 kg CO2/kg (average)
        """
        
        electricity_consumption = float(data.get('electricity_consumption', 0))
        natural_gas_consumption = float(data.get('natural_gas_consumption', 0))
        water_consumption = float(data.get('water_consumption', 0))
        waste_generated = float(data.get('waste_generated', 0))
        renewable_energy_percentage = float(data.get('renewable_energy_percentage', 0))
        
        # Emission factors
        ELECTRICITY_FACTOR = 0.82  # kg CO2/kWh
        NATURAL_GAS_FACTOR = 2.04  # kg CO2/m3
        WATER_FACTOR = 0.34  # kg CO2/m3
        WASTE_FACTOR = 0.5  # kg CO2/kg
        
        # Calculate emissions from each source
        electricity_emissions = electricity_consumption * ELECTRICITY_FACTOR
        
        # Adjust for renewable energy
        renewable_reduction = (electricity_emissions * renewable_energy_percentage) / 100
        electricity_emissions -= renewable_reduction
        
        natural_gas_emissions = natural_gas_consumption * NATURAL_GAS_FACTOR
        water_emissions = water_consumption * WATER_FACTOR
        waste_emissions = waste_generated * WASTE_FACTOR
        
        # Total carbon footprint
        total_carbon_footprint = (
            electricity_emissions + 
            natural_gas_emissions + 
            water_emissions + 
            waste_emissions
        )
        
        return {
            'electricity_emissions': round(electricity_emissions, 2),
            'natural_gas_emissions': round(natural_gas_emissions, 2),
            'water_emissions': round(water_emissions, 2),
            'waste_emissions': round(waste_emissions, 2),
            'renewable_energy_offset': round(renewable_reduction, 2),
            'total_carbon_footprint': round(total_carbon_footprint, 2)
        }
    
    @staticmethod
    def find_by_id(audit_id):
        """Find audit by ID"""
        collection = CarbonEmissionAudit._get_collection()
        audit = collection.find_one({'_id': ObjectId(audit_id)})
        if audit:
            audit['_id'] = str(audit['_id'])
            audit['user_id'] = str(audit['user_id'])
        return audit
    
    @staticmethod
    def find_by_user(user_id, limit=50):
        """Find all audits for a user"""
        collection = CarbonEmissionAudit._get_collection()
        audits = list(collection.find(
            {'user_id': ObjectId(user_id)}
        ).sort('created_at', -1).limit(limit))
        
        for audit in audits:
            audit['_id'] = str(audit['_id'])
            audit['user_id'] = str(audit['user_id'])
        
        return audits
    
    @staticmethod
    def update_audit(audit_id, user_id, data):
        """Update existing audit"""
        collection = CarbonEmissionAudit._get_collection()
        
        # Recalculate emissions
        emissions = CarbonEmissionAudit.calculate_emissions(data)
        
        update_doc = {
            '$set': {
                'input_data': data,
                'emissions': emissions,
                'total_carbon_footprint': emissions['total_carbon_footprint'],
                'updated_at': datetime.utcnow()
            }
        }
        
        result = collection.update_one(
            {'_id': ObjectId(audit_id), 'user_id': ObjectId(user_id)},
            update_doc
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def delete_audit(audit_id, user_id):
        """Delete audit"""
        collection = CarbonEmissionAudit._get_collection()
        result = collection.delete_one({
            '_id': ObjectId(audit_id),
            'user_id': ObjectId(user_id)
        })
        return result.deleted_count > 0
    
    @staticmethod
    def to_dict(audit):
        """Convert audit document to dictionary"""
        if not audit:
            return None
        
        return {
            'id': str(audit['_id']),
            'user_id': str(audit['user_id']),
            'facility_name': audit['facility_name'],
            'audit_period': audit['audit_period'],
            'input_data': audit['input_data'],
            'emissions': audit['emissions'],
            'total_carbon_footprint': audit['total_carbon_footprint'],
            'created_at': audit['created_at'].isoformat(),
            'updated_at': audit['updated_at'].isoformat(),
            'status': audit['status']
        }
