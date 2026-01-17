from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.carbon_emission_audit import CarbonEmissionAudit
from app.models.igbc_green_building_audit import IGBCGreenBuildingAudit
from app.models.esg_audit import ESGAudit

bp = Blueprint('audits', __name__, url_prefix='/api/audits')


# ==================== CARBON EMISSION AUDITS ====================

@bp.route('/carbon/create', methods=['POST'])
@jwt_required()
def create_carbon_audit():
    """Create a new carbon emission audit"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['facility_name', 'audit_period']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        audit_id = CarbonEmissionAudit.create_audit(
            user_id,
            data['facility_name'],
            data['audit_period'],
            data.get('audit_data', {})
        )
        
        audit = CarbonEmissionAudit.find_by_id(audit_id)
        
        return jsonify({
            'success': True,
            'message': 'Carbon audit created successfully',
            'audit': CarbonEmissionAudit.to_dict(audit)
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@bp.route('/carbon/<audit_id>', methods=['GET'])
@jwt_required()
def get_carbon_audit(audit_id):
    """Get carbon audit by ID"""
    try:
        user_id = get_jwt_identity()
        audit = CarbonEmissionAudit.find_by_id(audit_id)
        
        if not audit or str(audit['user_id']) != str(user_id):
            return jsonify({'success': False, 'message': 'Audit not found'}), 404
        
        return jsonify({
            'success': True,
            'audit': CarbonEmissionAudit.to_dict(audit)
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@bp.route('/carbon/list', methods=['GET'])
@jwt_required()
def list_carbon_audits():
    """List all carbon audits for user"""
    try:
        user_id = get_jwt_identity()
        audits = CarbonEmissionAudit.find_by_user(user_id)
        
        return jsonify({
            'success': True,
            'count': len(audits),
            'audits': [CarbonEmissionAudit.to_dict(a) for a in audits]
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@bp.route('/carbon/<audit_id>', methods=['PUT'])
@jwt_required()
def update_carbon_audit(audit_id):
    """Update carbon audit"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        success = CarbonEmissionAudit.update_audit(audit_id, user_id, data.get('audit_data', {}))
        
        if not success:
            return jsonify({'success': False, 'message': 'Audit not found or unauthorized'}), 404
        
        audit = CarbonEmissionAudit.find_by_id(audit_id)
        
        return jsonify({
            'success': True,
            'message': 'Carbon audit updated successfully',
            'audit': CarbonEmissionAudit.to_dict(audit)
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@bp.route('/carbon/<audit_id>', methods=['DELETE'])
@jwt_required()
def delete_carbon_audit(audit_id):
    """Delete carbon audit"""
    try:
        user_id = get_jwt_identity()
        
        success = CarbonEmissionAudit.delete_audit(audit_id, user_id)
        
        if not success:
            return jsonify({'success': False, 'message': 'Audit not found or unauthorized'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Carbon audit deleted successfully'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== IGBC GREEN BUILDING AUDITS ====================

@bp.route('/igbc/create', methods=['POST'])
@jwt_required()
def create_igbc_audit():
    """Create a new IGBC Green Building audit"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['building_name', 'audit_period']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        audit_id = IGBCGreenBuildingAudit.create_audit(
            user_id,
            data['building_name'],
            data['audit_period'],
            data.get('audit_data', {})
        )
        
        audit = IGBCGreenBuildingAudit.find_by_id(audit_id)
        
        return jsonify({
            'success': True,
            'message': 'IGBC audit created successfully',
            'audit': IGBCGreenBuildingAudit.to_dict(audit)
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@bp.route('/igbc/<audit_id>', methods=['GET'])
@jwt_required()
def get_igbc_audit(audit_id):
    """Get IGBC audit by ID"""
    try:
        user_id = get_jwt_identity()
        audit = IGBCGreenBuildingAudit.find_by_id(audit_id)
        
        if not audit or str(audit['user_id']) != str(user_id):
            return jsonify({'success': False, 'message': 'Audit not found'}), 404
        
        return jsonify({
            'success': True,
            'audit': IGBCGreenBuildingAudit.to_dict(audit)
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@bp.route('/igbc/list', methods=['GET'])
@jwt_required()
def list_igbc_audits():
    """List all IGBC audits for user"""
    try:
        user_id = get_jwt_identity()
        audits = IGBCGreenBuildingAudit.find_by_user(user_id)
        
        return jsonify({
            'success': True,
            'count': len(audits),
            'audits': [IGBCGreenBuildingAudit.to_dict(a) for a in audits]
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@bp.route('/igbc/<audit_id>', methods=['PUT'])
@jwt_required()
def update_igbc_audit(audit_id):
    """Update IGBC audit"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        success = IGBCGreenBuildingAudit.update_audit(audit_id, user_id, data.get('audit_data', {}))
        
        if not success:
            return jsonify({'success': False, 'message': 'Audit not found or unauthorized'}), 404
        
        audit = IGBCGreenBuildingAudit.find_by_id(audit_id)
        
        return jsonify({
            'success': True,
            'message': 'IGBC audit updated successfully',
            'audit': IGBCGreenBuildingAudit.to_dict(audit)
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@bp.route('/igbc/<audit_id>', methods=['DELETE'])
@jwt_required()
def delete_igbc_audit(audit_id):
    """Delete IGBC audit"""
    try:
        user_id = get_jwt_identity()
        
        success = IGBCGreenBuildingAudit.delete_audit(audit_id, user_id)
        
        if not success:
            return jsonify({'success': False, 'message': 'Audit not found or unauthorized'}), 404
        
        return jsonify({
            'success': True,
            'message': 'IGBC audit deleted successfully'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== ESG AUDITS ====================

@bp.route('/esg/create', methods=['POST'])
@jwt_required()
def create_esg_audit():
    """Create a new ESG audit"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['organization_name', 'audit_period']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        audit_id = ESGAudit.create_audit(
            user_id,
            data['organization_name'],
            data['audit_period'],
            data.get('audit_data', {})
        )
        
        audit = ESGAudit.find_by_id(audit_id)
        
        return jsonify({
            'success': True,
            'message': 'ESG audit created successfully',
            'audit': ESGAudit.to_dict(audit)
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@bp.route('/esg/<audit_id>', methods=['GET'])
@jwt_required()
def get_esg_audit(audit_id):
    """Get ESG audit by ID"""
    try:
        user_id = get_jwt_identity()
        audit = ESGAudit.find_by_id(audit_id)
        
        if not audit or str(audit['user_id']) != str(user_id):
            return jsonify({'success': False, 'message': 'Audit not found'}), 404
        
        return jsonify({
            'success': True,
            'audit': ESGAudit.to_dict(audit)
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@bp.route('/esg/list', methods=['GET'])
@jwt_required()
def list_esg_audits():
    """List all ESG audits for user"""
    try:
        user_id = get_jwt_identity()
        audits = ESGAudit.find_by_user(user_id)
        
        return jsonify({
            'success': True,
            'count': len(audits),
            'audits': [ESGAudit.to_dict(a) for a in audits]
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@bp.route('/esg/<audit_id>', methods=['PUT'])
@jwt_required()
def update_esg_audit(audit_id):
    """Update ESG audit"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        success = ESGAudit.update_audit(audit_id, user_id, data.get('audit_data', {}))
        
        if not success:
            return jsonify({'success': False, 'message': 'Audit not found or unauthorized'}), 404
        
        audit = ESGAudit.find_by_id(audit_id)
        
        return jsonify({
            'success': True,
            'message': 'ESG audit updated successfully',
            'audit': ESGAudit.to_dict(audit)
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@bp.route('/esg/<audit_id>', methods=['DELETE'])
@jwt_required()
def delete_esg_audit(audit_id):
    """Delete ESG audit"""
    try:
        user_id = get_jwt_identity()
        
        success = ESGAudit.delete_audit(audit_id, user_id)
        
        if not success:
            return jsonify({'success': False, 'message': 'Audit not found or unauthorized'}), 404
        
        return jsonify({
            'success': True,
            'message': 'ESG audit deleted successfully'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
