from datetime import datetime
from bson import ObjectId
from app.db.mongo import MongoDB


class IGBCGreenBuildingAudit:
    """Model for IGBC Green Building Audit"""
    
    COLLECTION_NAME = 'igbc_green_building_audits'
    
    @staticmethod
    def _get_collection():
        """Get MongoDB collection"""
        return MongoDB.get_collection(IGBCGreenBuildingAudit.COLLECTION_NAME)
    
    @staticmethod
    def create_indexes():
        """Create database indexes"""
        collection = IGBCGreenBuildingAudit._get_collection()
        collection.create_index("user_id")
        collection.create_index("created_at")
        collection.create_index("building_name")
    
    @staticmethod
    def create_audit(user_id, building_name, audit_period, data):
        """Create a new IGBC Green Building audit
        
        Args:
            user_id: User ID (ObjectId)
            building_name: Name of building being audited
            audit_period: Period of audit
            data: Dictionary containing IGBC parameters
        
        Returns:
            Inserted audit ID
        """
        # Calculate scores
        scores = IGBCGreenBuildingAudit.calculate_scores(data)
        
        audit_doc = {
            'user_id': ObjectId(user_id),
            'building_name': building_name,
            'audit_period': audit_period,
            'input_data': data,
            'scores': scores,
            'total_score': scores['total_score'],
            'rating': scores['rating'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'status': 'completed'
        }
        
        collection = IGBCGreenBuildingAudit._get_collection()
        result = collection.insert_one(audit_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def calculate_scores(data):
        """Calculate IGBC Green Building scores based on input data
        
        IGBC Categories (out of 100 points):
        - Site Selection & Planning (10)
        - Water Conservation (10)
        - Energy Conservation (15)
        - Environment Protection (10)
        - Health & Wellbeing (10)
        - Construction Practices (10)
        - Management & Operations (10)
        - Innovation (5)
        """
        
        # Get scores from input data
        site_score = float(data.get('site_selection', 0))
        water_score = float(data.get('water_conservation', 0))
        energy_score = float(data.get('energy_conservation', 0))
        environment_score = float(data.get('environment_protection', 0))
        health_score = float(data.get('health_wellbeing', 0))
        construction_score = float(data.get('construction_practices', 0))
        management_score = float(data.get('management_operations', 0))
        innovation_score = float(data.get('innovation', 0))
        
        # Verify scores are within ranges
        site_score = min(site_score, 10)
        water_score = min(water_score, 10)
        energy_score = min(energy_score, 15)
        environment_score = min(environment_score, 10)
        health_score = min(health_score, 10)
        construction_score = min(construction_score, 10)
        management_score = min(management_score, 10)
        innovation_score = min(innovation_score, 5)
        
        # Calculate total score (out of 100)
        total_score = (
            site_score + 
            water_score + 
            energy_score + 
            environment_score + 
            health_score + 
            construction_score + 
            management_score + 
            innovation_score
        )
        
        # Determine rating based on total score
        if total_score >= 85:
            rating = 'PLATINUM'
        elif total_score >= 70:
            rating = 'GOLD'
        elif total_score >= 55:
            rating = 'SILVER'
        elif total_score >= 40:
            rating = 'GREEN'
        else:
            rating = 'NOT RATED'
        
        return {
            'site_selection': round(site_score, 2),
            'water_conservation': round(water_score, 2),
            'energy_conservation': round(energy_score, 2),
            'environment_protection': round(environment_score, 2),
            'health_wellbeing': round(health_score, 2),
            'construction_practices': round(construction_score, 2),
            'management_operations': round(management_score, 2),
            'innovation': round(innovation_score, 2),
            'total_score': round(total_score, 2),
            'rating': rating
        }
    
    @staticmethod
    def find_by_id(audit_id):
        """Find audit by ID"""
        collection = IGBCGreenBuildingAudit._get_collection()
        audit = collection.find_one({'_id': ObjectId(audit_id)})
        if audit:
            audit['_id'] = str(audit['_id'])
            audit['user_id'] = str(audit['user_id'])
        return audit
    
    @staticmethod
    def find_by_user(user_id, limit=50):
        """Find all audits for a user"""
        collection = IGBCGreenBuildingAudit._get_collection()
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
        collection = IGBCGreenBuildingAudit._get_collection()
        
        # Recalculate scores
        scores = IGBCGreenBuildingAudit.calculate_scores(data)
        
        update_doc = {
            '$set': {
                'input_data': data,
                'scores': scores,
                'total_score': scores['total_score'],
                'rating': scores['rating'],
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
        collection = IGBCGreenBuildingAudit._get_collection()
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
            'building_name': audit['building_name'],
            'audit_period': audit['audit_period'],
            'input_data': audit['input_data'],
            'scores': audit['scores'],
            'total_score': audit['total_score'],
            'rating': audit['rating'],
            'created_at': audit['created_at'].isoformat(),
            'updated_at': audit['updated_at'].isoformat(),
            'status': audit['status']
        }
