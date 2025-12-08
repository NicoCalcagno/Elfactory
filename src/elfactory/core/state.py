"""WorkshopState - Shared state management for gift production."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class ChildInfo(BaseModel):
    """Information about the child requesting the gift."""
    name: str
    age: int | None = None
    location: str | None = None
    behavior_score: str | None = None


class Component(BaseModel):
    """A single component created by an artisan elf."""
    id: str
    type: str
    material: str
    dimensions: str
    details: str
    created_by: str
    status: str = "completed"
    timestamp: datetime = Field(default_factory=datetime.now)


class ManufacturingLogEntry(BaseModel):
    """Log entry for manufacturing actions."""
    timestamp: datetime = Field(default_factory=datetime.now)
    agent: str
    action: str
    details: str


class Issue(BaseModel):
    """Issue or problem encountered during production."""
    timestamp: datetime = Field(default_factory=datetime.now)
    reported_by: str
    severity: str
    description: str
    resolved: bool = False


class QualityReport(BaseModel):
    """Quality inspection report."""
    inspector: str = "quality_manager"
    timestamp: datetime = Field(default_factory=datetime.now)
    overall_status: str
    components_checked: int = 0
    issues_found: list[str] = Field(default_factory=list)
    safety_approved: bool = False
    notes: str = ""


class WorkshopState(BaseModel):
    """Shared state for gift production workflow."""

    gift_id: str | None = None
    status: str = "initialized"

    child_info: ChildInfo | None = None
    gift_request: str = ""
    sender_email: str = ""  # Email address to send the response to

    feasibility: str = "unknown"
    manufacturing_decision: str = "pending"

    blueprint: str = ""
    bill_of_materials: list[dict[str, Any]] = Field(default_factory=list)

    components: list[Component] = Field(default_factory=list)
    manufacturing_log: list[ManufacturingLogEntry] = Field(default_factory=list)
    issues: list[Issue] = Field(default_factory=list)

    quality_report: QualityReport | None = None

    packaging_design: str = ""
    gift_card_message: str = ""

    image_prompt: str = ""
    image_url: str = ""

    santa_approval: dict[str, Any] = Field(default_factory=dict)

    final_response: str = ""

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def add_component(self, component_data: dict[str, Any]) -> None:
        """Add a component to the production."""
        component = Component(**component_data)
        self.components.append(component)
        self.updated_at = datetime.now()

    def log_action(self, agent: str, action: str, details: str) -> None:
        """Log a manufacturing action."""
        entry = ManufacturingLogEntry(
            agent=agent,
            action=action,
            details=details
        )
        self.manufacturing_log.append(entry)
        self.updated_at = datetime.now()

    def add_issue(self, reported_by: str, severity: str, description: str) -> None:
        """Report an issue during production."""
        issue = Issue(
            reported_by=reported_by,
            severity=severity,
            description=description
        )
        self.issues.append(issue)
        self.updated_at = datetime.now()

    def resolve_issue(self, issue_index: int) -> None:
        """Mark an issue as resolved."""
        if 0 <= issue_index < len(self.issues):
            self.issues[issue_index].resolved = True
            self.updated_at = datetime.now()

    def update_status(self, new_status: str) -> None:
        """Update the overall production status."""
        self.status = new_status
        self.updated_at = datetime.now()

    def set_quality_report(self, report_data: dict[str, Any]) -> None:
        """Set the quality inspection report."""
        self.quality_report = QualityReport(**report_data)
        self.updated_at = datetime.now()

    def to_summary(self) -> str:
        """Generate a human-readable summary of the current state."""
        summary = f"Gift ID: {self.gift_id}\n"
        summary += f"Status: {self.status}\n"
        summary += f"Child: {self.child_info.name if self.child_info else 'Unknown'}\n"
        summary += f"Request: {self.gift_request[:100]}...\n" if len(self.gift_request) > 100 else f"Request: {self.gift_request}\n"
        summary += f"Components: {len(self.components)}\n"
        summary += f"Manufacturing Decision: {self.manufacturing_decision}\n"
        summary += f"Issues: {len([i for i in self.issues if not i.resolved])} unresolved\n"
        return summary
