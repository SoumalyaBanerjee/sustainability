from datetime import datetime
from bson import ObjectId
from app.db.mongo import MongoDB


class ESGAudit:
    """Model for ESG (Environmental, Social, Governance) Audit"""
    
    COLLECTION_NAME = 'esg_audits'
    
    @staticmethod
    def _get_collection():
        """Get MongoDB collection"""
        return MongoDB.get_collection(ESGAudit.COLLECTION_NAME)
    
    @staticmethod
    def create_indexes():
        """Create database indexes"""
        collection = ESGAudit._get_collection()
        collection.create_index("user_id")
        collection.create_index("created_at")
        collection.create_index("organization_name")
    
    @staticmethod
    def create_audit(user_id, organization_name, audit_period, data):
        """Create a new ESG audit
        
        Args:
            user_id: User ID (ObjectId)
            organization_name: Name of organization being audited
            audit_period: Period of audit
            data: Dictionary containing ESG parameters
        
        Returns:
            Inserted audit ID
        """
        # Calculate scores
        scores = ESGAudit.calculate_scores(data)
        
        audit_doc = {
            'user_id': ObjectId(user_id),
            'organization_name': organization_name,
            'audit_period': audit_period,
            'input_data': data,
            'scores': scores,
            'environmental_score': scores['environmental_score'],
            'social_score': scores['social_score'],
            'governance_score': scores['governance_score'],
            'esg_score': scores['esg_score'],
            'esg_rating': scores['esg_rating'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'status': 'completed'
        }
        
        collection = ESGAudit._get_collection()
        result = collection.insert_one(audit_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def calculate_scores(data):
        """Calculate ESG scores based on input data
        
        ESG Categories (each out of 100):
        - Environmental: Carbon, Water, Waste Management, Renewable Energy
        - Social: Employee Satisfaction, Community Impact, Health & Safety, Diversity
        - Governance: Ethics, Compliance, Board Diversity, Transparency
        """
        
        # Environmental Score
        carbon_management = float(data.get('carbon_management', 0))
        water_management = float(data.get('water_management', 0))
        waste_management = float(data.get('waste_management', 0))
        renewable_energy = float(data.get('renewable_energy', 0))
        
        environmental_score = (
            (carbon_management * 0.3) +
            (water_management * 0.3) +
            (waste_management * 0.2) +
            (renewable_energy * 0.2)
        )
        
        # Social Score
        employee_satisfaction = float(data.get('employee_satisfaction', 0))
        community_impact = float(data.get('community_impact', 0))
        health_safety = float(data.get('health_safety', 0))
        diversity_inclusion = float(data.get('diversity_inclusion', 0))
        
        social_score = (
            (employee_satisfaction * 0.3) +
            (community_impact * 0.3) +
            (health_safety * 0.2) +
            (diversity_inclusion * 0.2)
        )
        
        # Governance Score
        ethics_compliance = float(data.get('ethics_compliance', 0))
        audit_controls = float(data.get('audit_controls', 0))
        board_diversity = float(data.get('board_diversity', 0))
        transparency = float(data.get('transparency', 0))
        
        governance_score = (
            (ethics_compliance * 0.35) +
            (audit_controls * 0.35) +
            (board_diversity * 0.15) +
            (transparency * 0.15)
        )
        
        # Overall ESG Score (average of E, S, G)
        esg_score = (environmental_score + social_score + governance_score) / 3
        
        # Determine ESG Rating
        if esg_score >= 80:
            esg_rating = 'EXCELLENT'
        elif esg_score >= 70:
            esg_rating = 'VERY GOOD'
        elif esg_score >= 60:
            esg_rating = 'GOOD'
        elif esg_score >= 50:
            esg_rating = 'ADEQUATE'
        else:
            esg_rating = 'NEEDS IMPROVEMENT'
        
        return {
            'environmental_score': round(environmental_score, 2),
            'social_score': round(social_score, 2),
            'governance_score': round(governance_score, 2),
            'esg_score': round(esg_score, 2),
            'esg_rating': esg_rating,
            'environmental_details': {
                'carbon_management': round(carbon_management, 2),
                'water_management': round(water_management, 2),
                'waste_management': round(waste_management, 2),
                'renewable_energy': round(renewable_energy, 2)
            },
            'social_details': {
                'employee_satisfaction': round(employee_satisfaction, 2),
                'community_impact': round(community_impact, 2),
                'health_safety': round(health_safety, 2),
                'diversity_inclusion': round(diversity_inclusion, 2)
            },
            'governance_details': {
                'ethics_compliance': round(ethics_compliance, 2),
                'audit_controls': round(audit_controls, 2),
                'board_diversity': round(board_diversity, 2),
                'transparency': round(transparency, 2)
            }
        }
    
    @staticmethod
    def find_by_id(audit_id):
        """Find audit by ID"""
        collection = ESGAudit._get_collection()
        audit = collection.find_one({'_id': ObjectId(audit_id)})
        if audit:
            audit['_id'] = str(audit['_id'])
            audit['user_id'] = str(audit['user_id'])
        return audit
    
    @staticmethod
    def find_by_user(user_id, limit=50):
        """Find all audits for a user"""
        collection = ESGAudit._get_collection()
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
        collection = ESGAudit._get_collection()
        
        # Recalculate scores
        scores = ESGAudit.calculate_scores(data)
        
        update_doc = {
            '$set': {
                'input_data': data,
                'scores': scores,
                'environmental_score': scores['environmental_score'],
                'social_score': scores['social_score'],
                'governance_score': scores['governance_score'],
                'esg_score': scores['esg_score'],
                'esg_rating': scores['esg_rating'],
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
        collection = ESGAudit._get_collection()
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
            'organization_name': audit['organization_name'],
            'audit_period': audit['audit_period'],
            'input_data': audit['input_data'],
            'scores': audit['scores'],
            'environmental_score': audit['environmental_score'],
            'social_score': audit['social_score'],
            'governance_score': audit['governance_score'],
            'esg_score': audit['esg_score'],
            'esg_rating': audit['esg_rating'],
            'created_at': audit['created_at'].isoformat(),
            'updated_at': audit['updated_at'].isoformat(),
            'status': audit['status']
        }
