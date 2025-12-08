"""Test the complete gift workflow end-to-end.

This script tests the Elfactory workflow by processing a sample gift request
and verifying that all stages complete successfully.
"""

import sys
from elfactory.core.orchestrator import process_gift_request
from elfactory.utils import setup_logging
from elfactory.config import settings


def main():
    """Run workflow test."""
    # Setup logging
    logger = setup_logging(log_level="INFO")

    print("\n")
    print("🎄" * 40)
    print("ELFACTORY WORKFLOW TEST")
    print("🎄" * 40)
    print("\n")

    # Test gift request - use from env if provided, otherwise use default
    email_content = settings.test_email_content or """
    Caro Babbo Natale,

    mi chiamo Marco, ho 8 anni e abito a Milano.
    Per Natale vorrei una macchinina telecomandata rossa.

    Grazie!
    Marco
    """

    print("Processing gift request...")
    print("=" * 80)
    print(email_content.strip())
    print("=" * 80)
    print()

    # Get test recipient email from settings
    recipient_email = settings.test_recipient_email
    if recipient_email:
        print(f"Test mode: Will send response to {recipient_email}")
        print()

    try:
        state = process_gift_request(email_content, recipient_email)

        print()
        print("=" * 80)
        print("WORKFLOW COMPLETED")
        print("=" * 80)
        print(f"Gift ID: {state.gift_id}")
        print(f"Final Status: {state.status}")
        print(f"Child: {state.child_info.name if state.child_info else 'Unknown'}")
        print(f"Age: {state.child_info.age if state.child_info else 'Unknown'}")
        print(f"Location: {state.child_info.location if state.child_info else 'Unknown'}")
        print()
        print(f"Feasibility: {state.feasibility}")
        print(f"Manufacturing Decision: {state.manufacturing_decision}")
        print(f"Blueprint: {'Yes' if state.blueprint else 'No'}")
        print()
        print(f"Components Created: {len(state.components)}")
        print(f"Manufacturing Log Entries: {len(state.manufacturing_log)}")
        print(f"Issues: {len([i for i in state.issues if not i.resolved])} unresolved")
        print(f"Quality Report: {'Yes' if state.quality_report else 'No'}")
        print(f"Final Response: {'Yes' if state.final_response else 'No'}")
        print("=" * 80)
        print()

        # Show components
        if state.components:
            print("Components Created:")
            print("-" * 80)
            for comp in state.components:
                print(f"  • {comp.id} ({comp.type}) - {comp.material}")
                print(f"    Created by: {comp.created_by}")
            print("=" * 80)
            print()

        # Show manufacturing log summary
        if state.manufacturing_log:
            print("Manufacturing Log (last 10 entries):")
            print("-" * 80)
            for entry in state.manufacturing_log[-10:]:
                print(f"  [{entry.timestamp.strftime('%H:%M:%S')}] {entry.agent}")
                print(f"    → {entry.action}")
            print("=" * 80)
            print()

        # Verify success
        success = (
            state.status in ["completed", "delivered", "approved", "ready_for_delivery"] and
            state.child_info is not None and
            len(state.components) > 0 and
            state.final_response
        )

        print()
        print("=" * 80)
        print(f"TEST RESULT: {'✓ PASSED' if success else '✗ FAILED'}")
        print("=" * 80)
        print()

        if success:
            print("✓ All workflow stages completed successfully!")
            print("✓ Gift was processed from request to final response")
            print()
            return 0
        else:
            print("✗ Workflow did not complete all expected stages")
            print(f"  Final status: {state.status}")
            print(f"  Expected: completed/delivered/approved/ready_for_delivery")
            print()
            return 1

    except Exception as e:
        print()
        print("=" * 80)
        print("✗ TEST FAILED WITH ERROR")
        print("=" * 80)
        print(f"Error: {type(e).__name__}: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
