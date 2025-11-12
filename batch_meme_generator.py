"""
Batch meme generator for predefined workplace situations
"""
from meme_forge import MemeForge
import json
import os

# Predefined workplace situations for quick testing
WORKPLACE_SITUATIONS = [
    "When you fix a bug but create three new ones",
    "When the client says 'quick change' on Friday at 5pm",
    "When you're the only one in a meeting who read the agenda",
    "When the internet goes down and you realize how much you depend on it",
    "When someone schedules a meeting that could have been an email",
    "When you finally understand a complex piece of legacy code",
    "When deployment works in dev but fails in production",
    "When you're asked to give an estimate without any requirements",
    "When the coffee machine breaks on Monday morning",
    "When you spend 3 hours debugging and the issue is a missing semicolon"
]

def generate_batch_memes():
    """Generate memes for all predefined situations"""
    
    forge = MemeForge()
    results = []
    
    print("🔥 Batch Meme Generation Started! 🔥")
    print(f"Generating {len(WORKPLACE_SITUATIONS)} memes...")
    print("=" * 50)
    
    for i, situation in enumerate(WORKPLACE_SITUATIONS, 1):
        print(f"\n[{i}/{len(WORKPLACE_SITUATIONS)}] Processing...")
        
        try:
            result = forge.create_meme(situation)
            if result:
                results.append(result)
                print(f"✅ Success!")
            else:
                print(f"❌ Failed")
        except Exception as e:
            print(f"❌ Error: {e}")
        print("-" * 30)
    
    # Save results summary
    summary = {
        "total_generated": len(results),
        "total_requested": len(WORKPLACE_SITUATIONS),
        "memes": results
    }
    
    os.makedirs("static/generated", exist_ok=True)
    with open("static/generated/batch_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n🎉 Batch generation complete!")
    print(f"Generated: {len(results)}/{len(WORKPLACE_SITUATIONS)} memes")
    print(f"Summary saved to: static/generated/batch_summary.json")
    
    return results


if __name__ == "__main__":
    generate_batch_memes()