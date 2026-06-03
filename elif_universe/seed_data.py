import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elif_platform.settings')
django.setup()

from discovery.models import Inquiry, Planet

def seed():
    # Clear existing data
    Inquiry.objects.all().delete()
    
    # Inquiry 1
    inq1 = Inquiry.objects.create(
        case_id="ELECTROCULTURE-01",
        core_question="How does atmospheric electricity affect seedling growth in drought conditions?",
    )
    
    planets = [
        ("Frame Validator", "fa-vial", 1, "COMPLETED"),
        ("Object Decomposer", "fa-dna", 2, "COMPLETED"),
        ("Hypothesis Validator", "fa-flask", 3, "IN_PROGRESS"),
        ("Roadmap Engine", "fa-route", 4, "NOT_STARTED"),
        ("Governance Kernel", "fa-shield-halved", 5, "NOT_STARTED"),
        ("Truth Separator", "fa-eye", 6, "NOT_STARTED"),
        ("Feedback Logger", "fa-clipboard-list", 7, "NOT_STARTED"),
    ]
    
    for name, icon, order, status in planets:
        Planet.objects.create(
            inquiry=inq1,
            name=name,
            icon_class=icon,
            order=order,
            status=status,
            data={"analysis": "Pre-seeded data for visualization."} if status == "COMPLETED" else {}
        )

    # Inquiry 2
    inq2 = Inquiry.objects.create(
        case_id="POLICY-GOV-02",
        core_question="Can decentralized autonomous organizations (DAOs) manage common-pool resources effectively?",
    )
    
    for name, icon, order, status in planets:
        Planet.objects.create(
            inquiry=inq2,
            name=name,
            icon_class=icon,
            order=order,
            status="NOT_STARTED"
        )

    print("Universe seeded with 2 active systems.")

if __name__ == "__main__":
    seed()
