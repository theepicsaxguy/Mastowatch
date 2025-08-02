from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from app.auth import get_api_key
from app.enhanced_scanning import EnhancedScanningSystem
from app.schemas import ScanSession, DomainAlert

router = APIRouter()

@router.post("/scan/start", response_model=ScanSession, status_code=status.HTTP_201_CREATED)
async def start_scan_session(session_type: str, api_key: str = Depends(get_api_key)):
    """Start a new scan session."""
    if session_type not in ["remote", "local", "federated"]:
        raise HTTPException(status_code=400, detail="Invalid session type")
    scanner = EnhancedScanningSystem()
    session_id = scanner.start_scan_session(session_type)
    return {"session_id": session_id, "session_type": session_type, "status": "started"}

@router.post("/scan/{session_id}/complete", status_code=status.HTTP_200_OK)
async def complete_scan_session(session_id: str, api_key: str = Depends(get_api_key)):
    """Complete a scan session."""
    scanner = EnhancedScanningSystem()
    scanner.complete_scan_session(session_id)
    return {"message": f"Session {session_id} completed"}

@router.get("/scan/accounts", response_model=List[Dict[str, Any]])
async def get_next_accounts_to_scan(session_type: str, limit: int = 50, cursor: str = None, api_key: str = Depends(get_api_key)):
    """Get the next batch of accounts to scan."""
    scanner = EnhancedScanningSystem()
    accounts, next_cursor = scanner.get_next_accounts_to_scan(session_type, limit, cursor)
    return accounts

@router.post("/scan/account", response_model=Dict[str, Any])
async def scan_account_efficiently(account_data: Dict[str, Any], session_id: str, api_key: str = Depends(get_api_key)):
    """Scan a single account efficiently."""
    scanner = EnhancedScanningSystem()
    result = scanner.scan_account_efficiently(account_data, session_id)
    return result

@router.get("/scan/federated", response_model=List[Dict[str, Any]])
async def scan_federated_content(target_domains: List[str] = None, api_key: str = Depends(get_api_key)):
    """Scan federated content."""
    scanner = EnhancedScanningSystem()
    results = scanner.scan_federated_content(target_domains)
    return results

@router.get("/domains/alerts", response_model=List[DomainAlert])
async def get_domain_alerts(limit: int = 100, api_key: str = Depends(get_api_key)):
    """Get domain alerts."""
    scanner = EnhancedScanningSystem()
    alerts = scanner.get_domain_alerts(limit)
    return alerts
