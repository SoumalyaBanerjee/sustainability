/**
 * Audit API Client
 * Handles all audit-related API calls
 */

class AuditAPI {
    constructor(baseURL = 'http://localhost:5000') {
        this.baseURL = baseURL;
        this.apiURL = `${baseURL}/api/audits`;
    }

    async request(method, endpoint, data = null) {
        const token = localStorage.getItem('authToken');
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${this.apiURL}${endpoint}`, options);
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // ==================== CARBON EMISSION AUDITS ====================

    async createCarbonAudit(facilityName, auditPeriod, auditData) {
        return this.request('POST', '/carbon/create', {
            facility_name: facilityName,
            audit_period: auditPeriod,
            audit_data: auditData
        });
    }

    async getCarbonAudit(auditId) {
        return this.request('GET', `/carbon/${auditId}`);
    }

    async listCarbonAudits() {
        return this.request('GET', '/carbon/list');
    }

    async updateCarbonAudit(auditId, auditData) {
        return this.request('PUT', `/carbon/${auditId}`, {
            audit_data: auditData
        });
    }

    async deleteCarbonAudit(auditId) {
        return this.request('DELETE', `/carbon/${auditId}`);
    }

    // ==================== IGBC GREEN BUILDING AUDITS ====================

    async createIGBCAudit(buildingName, auditPeriod, auditData) {
        return this.request('POST', '/igbc/create', {
            building_name: buildingName,
            audit_period: auditPeriod,
            audit_data: auditData
        });
    }

    async getIGBCAudit(auditId) {
        return this.request('GET', `/igbc/${auditId}`);
    }

    async listIGBCAudits() {
        return this.request('GET', '/igbc/list');
    }

    async updateIGBCAudit(auditId, auditData) {
        return this.request('PUT', `/igbc/${auditId}`, {
            audit_data: auditData
        });
    }

    async deleteIGBCAudit(auditId) {
        return this.request('DELETE', `/igbc/${auditId}`);
    }

    // ==================== ESG AUDITS ====================

    async createESGAudit(organizationName, auditPeriod, auditData) {
        return this.request('POST', '/esg/create', {
            organization_name: organizationName,
            audit_period: auditPeriod,
            audit_data: auditData
        });
    }

    async getESGAudit(auditId) {
        return this.request('GET', `/esg/${auditId}`);
    }

    async listESGAudits() {
        return this.request('GET', '/esg/list');
    }

    async updateESGAudit(auditId, auditData) {
        return this.request('PUT', `/esg/${auditId}`, {
            audit_data: auditData
        });
    }

    async deleteESGAudit(auditId) {
        return this.request('DELETE', `/esg/${auditId}`);
    }
}

// Initialize audit API
const auditAPI = new AuditAPI();
