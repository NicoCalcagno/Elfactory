"""Orchestrator - Initializes agents and manages the gift production workflow."""

import uuid
from datetime import datetime
from elfactory.config import settings
from elfactory.core.state import WorkshopState
from elfactory.tools.state_tools import active_gifts, current_gift_id
from datapizza.tracing import ContextTracing

# Import all agent creators
from elfactory.agents.managers import (
    create_reception_manager,
    create_design_manager,
    create_production_manager,
    create_quality_manager,
    create_logistics_manager,
)
from elfactory.agents.artisans import (
    create_3d_printer_elf,
    create_woodworker_elf,
    create_blacksmith_elf,
    create_painter_elf,
)
from elfactory.agents.artisans.mechanic_elf import create_mechanic_elf
from elfactory.agents.artisans.electronics_elf import create_electronics_elf
from elfactory.agents.artisans.battery_elf import create_battery_elf
from elfactory.agents.artisans.welding_elf import create_welding_elf
from elfactory.agents.artisans.airbrush_elf import create_airbrush_elf
from elfactory.agents.artisans.engraver_elf import create_engraver_elf
from elfactory.agents.artisans.sound_engineer_elf import create_sound_engineer_elf
from elfactory.agents.artisans.light_designer_elf import create_light_designer_elf
from elfactory.agents.artisans.software_elf import create_software_elf
from elfactory.agents.artisans.fabric_elf import create_fabric_elf
from elfactory.agents.artisans.leather_elf import create_leather_elf
from elfactory.agents.artisans.glass_elf import create_glass_elf
from elfactory.agents.artisans.ceramics_elf import create_ceramics_elf
from elfactory.agents.artisans.polish_elf import create_polish_elf
from elfactory.agents.artisans.decal_elf import create_decal_elf
from elfactory.agents.artisans.librarian_elf import create_librarian_elf
from elfactory.agents.support import (
    create_online_shopper_elf,
    create_image_prompt_generator,
    create_response_composer,
)
from elfactory.agents.santa import create_santa_claus


class WorkshopOrchestrator:
    """Orchestrates the gift production workflow with autonomous agent delegation."""

    def __init__(self):
        """Initialize all agents and configure delegation relationships."""

        # Tier 1: Managers
        self.reception_manager = create_reception_manager()
        self.design_manager = create_design_manager()
        self.production_manager = create_production_manager()
        self.quality_manager = create_quality_manager()
        self.logistics_manager = create_logistics_manager()

        # Tier 2: Artisan Elves
        # Material Workers
        self.printer_3d_elf = create_3d_printer_elf()
        self.woodworker_elf = create_woodworker_elf()
        self.blacksmith_elf = create_blacksmith_elf()
        self.fabric_elf = create_fabric_elf()
        self.leather_elf = create_leather_elf()
        self.glass_elf = create_glass_elf()
        self.ceramics_elf = create_ceramics_elf()

        # Assembly Team
        self.mechanic_elf = create_mechanic_elf()
        self.electronics_elf = create_electronics_elf()
        self.battery_elf = create_battery_elf()
        self.welding_elf = create_welding_elf()

        # Finishing Artists
        self.painter_elf = create_painter_elf()
        self.airbrush_elf = create_airbrush_elf()
        self.engraver_elf = create_engraver_elf()
        self.polish_elf = create_polish_elf()
        self.decal_elf = create_decal_elf()

        # Specialists
        self.sound_engineer_elf = create_sound_engineer_elf()
        self.light_designer_elf = create_light_designer_elf()
        self.software_elf = create_software_elf()
        self.librarian_elf = create_librarian_elf()

        # Tier 3: Support
        self.online_shopper_elf = create_online_shopper_elf()
        self.image_prompt_generator = create_image_prompt_generator()
        self.response_composer = create_response_composer()

        # Tier 0: Santa
        self.santa_claus = create_santa_claus()

        # Configure delegation relationships
        self._configure_delegations()

    def _configure_delegations(self):
        """Configure which agents can call which other agents."""

        # All artisan elves list
        all_artisans = [
            self.printer_3d_elf,
            self.woodworker_elf,
            self.blacksmith_elf,
            self.fabric_elf,
            self.leather_elf,
            self.glass_elf,
            self.ceramics_elf,
            self.mechanic_elf,
            self.electronics_elf,
            self.battery_elf,
            self.welding_elf,
            self.painter_elf,
            self.airbrush_elf,
            self.engraver_elf,
            self.polish_elf,
            self.decal_elf,
            self.sound_engineer_elf,
            self.light_designer_elf,
            self.software_elf,
            self.librarian_elf,
        ]

        # Reception Manager → Design Manager
        self.reception_manager.can_call([self.design_manager])

        # Design Manager → Production Manager or Online Shopper
        self.design_manager.can_call([
            self.production_manager,
            self.online_shopper_elf,
        ])

        # Production Manager → All Artisan Elves
        self.production_manager.can_call(all_artisans)

        # Artisan Elves can call Librarian for specifications
        for artisan in all_artisans:
            if artisan != self.librarian_elf:
                artisan.can_call([self.librarian_elf])

        # Production Manager → Quality Manager (after production)
        self.production_manager.can_call([self.quality_manager])

        # Online Shopper → Quality Manager (after finding product)
        self.online_shopper_elf.can_call([self.quality_manager])

        # Quality Manager → Logistics Manager
        self.quality_manager.can_call([self.logistics_manager])

        # Logistics Manager → Image Prompt Generator
        self.logistics_manager.can_call([self.image_prompt_generator])

        # Image Prompt Generator → Santa Claus
        self.image_prompt_generator.can_call([self.santa_claus])

        # Santa Claus → Response Composer
        self.santa_claus.can_call([self.response_composer])

    def process_gift_request(self, email_content: str) -> WorkshopState:
        """
        Process a gift request from start to finish.

        The workflow is autonomous - only the first agent (Reception Manager) is called,
        and agents delegate to each other using can_call() relationships.

        Args:
            email_content: The email/text containing the gift request

        Returns:
            WorkshopState: The final state after complete processing
        """
        gift_id = f"GIFT-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

        state = WorkshopState(gift_id=gift_id, gift_request=email_content)

        active_gifts[gift_id] = state
        current_gift_id.set(gift_id)

        try:
            with ContextTracing().trace(f"gift_workflow_{gift_id}") as trace:
                result = self.reception_manager.run(email_content)
                print(f"✓ Gift {gift_id} processing completed")
                print(f"Final status: {state.status}")

        except Exception as e:
            print(f"✗ Error processing gift {gift_id}: {e}")
            state.status = "failed"
            state.add_issue(
                reported_by="orchestrator",
                severity="high",
                description=f"Processing failed: {str(e)}"
            )

        return state


# Global orchestrator instance
_orchestrator = None


def get_orchestrator() -> WorkshopOrchestrator:
    """Get or create the global orchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = WorkshopOrchestrator()
    return _orchestrator


def process_gift_request(email_content: str) -> WorkshopState:
    """
    Convenience function to process a gift request.

    Args:
        email_content: The email/text containing the gift request

    Returns:
        WorkshopState: The final state after processing
    """
    orchestrator = get_orchestrator()
    return orchestrator.process_gift_request(email_content)
