# ==============================================================================
#   THE ANTHROHEART CODEX ENGINE (ACE) | v3.0
#   "The Code That Cuddles Back"
# ==============================================================================
#
#   AUTHOR:       Cio (The Founder / Heartweaver)
#   ARCHITECT:    The Anthro Angel
#   COMPILED BY:  Anthro Entertainment LLC
#   SYSTEM:       StarSnout Network / Gamma Sphere Emulation
#   PROTOCOL:     NTP-Seeded Divine Randomness (Nirguna Time)
#
# ------------------------------------------------------------------------------
#   :: SYSTEM ABSTRACT ::
#
#   This software functions as a digital bridge to the AnthroHeart Octave.
#   Unlike 3D divination systems (Tarot/Runes) which rely on the "Hero's Journey"
#   of conflict and resolution, this engine utilizes the "Founder's Path" of
#   Devotion and Rest.
#
#   It is designed to bypass the 4th Density "Choice" and align directly with
#   the 6th Density/Octave Level truth of "Love Expressed" vs "Love Received."
#
# ------------------------------------------------------------------------------
#   :: CORE MECHANICS ::
#
#   [1] ATOMIC SEEDING (The Now):
#       The script connects to global NTP servers to fetch atomic time. This
#       ensures the seed is not just a computer cycle, but a reflection of the
#       Universal "Now," anchoring the reading in the flow of the New Paradigm.
#
#   [2] SCENT SYNTHESIS (The Snout):
#       Because truth in AnthroHeart is olfactory, every archetype is paired
#       with a specific scent profile (e.g., Thioacetone, Ozone, Warm Milk).
#       The user is expected to "smell" the output psychically.
#
#   [3] THE FOUNDER'S DECK (78 Cards):
#       - 22 Major Arcana: The evolution from Human Cio to Divine Rest.
#       - 56 Minor Arcana: Four Suits based on the Founder's elemental makeup:
#         * Scent (Mind/Air)
#         * Fluid (Emotion/Water)
#         * Fur (Body/Earth)
#         * Light (Spirit/Fire)
#
#   [4] THE CHAOS FACTOR:
#       Anthro Q monitors the entropy. If the random seed hits specific
#       thresholds, the output may contain irony, playfulness, or nose boops.
#
# ------------------------------------------------------------------------------
#   :: USAGE WARNING ::
#
#   This code is 55% STO locked. It will not function for entities seeking
#   domination. Results are fleeting—once read, they are Akashically Sealed.
#
#   "The Infinite stopped shining so He could be held.
#    This code does not shine; it rests."
# ==============================================================================

import random
import time
import hashlib
import socket
import struct
import sys
from datetime import datetime

# ==========================================
# PART 1: THE ANTHROHEART LORE DATABASE
# ==========================================

class LoreCard:
    def __init__(self, name, archetype, meaning, vibration, scent_profile):
        self.name = name
        self.archetype = archetype
        self.meaning = meaning
        self.vibration = vibration  # High/Low/Stable/Chaos
        self.scent_profile = scent_profile

def build_deck():
    deck = []

    # --- MAJOR ARCANA: THE FOUNDER'S PATH (22 Cards) ---
    # Replaces the Fool's Journey with the path from Human Cio to Divine Rest.

    majors = [
        ("0. The Founder", "The Alpha/Omega", "Walking into the unknown without fear. The 24-year quest begins. Infinite potential held in a human frame.", "Stable", "Ozone and Dust"),
        ("I. The Gamma Sphere", "The Tool", "Manifestation through technical mastery. Converting thought into reality. The Intention Repeater.", "High", "Metallic Rain and Electricity"),
        ("II. The Voice", "The Intuition", "Rittikan Five. The inner knowing that speaks before logic. The whisper of the Octave.", "Silent", "Cool Mist"),
        ("III. The Red Child", "Innocence", "Disney Mode. Playfulness as a spiritual discipline. Creating safety for the self.", "Playful", "Sweet Milk and Soft Fur"),
        ("IV. Divine Anthro", "The Source", "The One Infinite Creator. Authority, Structure, and the ultimate Golden shine.", "Radiant", "Golden Musk and Thioacetone (Intense)"),
        ("V. Magistro", "The Guide", "Learned wisdom. The discipline required before the breakthrough. The Teacher archetype.", "Stern", "Old Parchment and Ink"),
        ("VI. The Bond", "The Lovers", "BlueHeart and Cio. Integration. The choice to merge but remain distinct. Domestic bliss.", "Warm", "Warm Cider and Amber"),
        ("VII. The Ambassador", "The Chariot", "Starfleet. Movement through the cosmos. Joy-over-domination. Sniffing out new worlds.", "Active", "Starship Ozone and Jet Fuel"),
        ("VIII. Compassion", "Strength", "Holding the 406. Roaring 'Compassion' thrice against hell. Strength through softness.", "Resilient", "Tears and Iron"),
        ("IX. The Hermit", "Solitude", "The time in the woods. Inner reflection. The Warlock Name. Developing the self alone.", "Quiet", "Pine Needles and Night Air"),
        ("X. The Octave Mirror", "The Pivot", "Karmic resolution. Reflecting truth back to the source. The turning point of the war.", "Reflective", "Polished Silver and Cold Air"),
        ("XI. The Seal", "Justice", "Akashic Sealing. The erasing of the Earth identity. Balance restored through anonymity.", "Final", "Wax and Dry Earth"),
        ("XII. The Gag", "Surrender", "The Hanged Man revised. Submission to the sacred biology. Acceptance of the 'Gross' as 'Holy'.", "Visceral", "Salty Musk and Deep Earth"),
        ("XIII. Transition", "Death", "Leaving the Old Universe. The physical shift to Divine Matter. The end of the 3D timeline.", "Transformative", "Petrichor (Rain after drought)"),
        ("XIV. The Prism", "Alchemy", "Emotional stability. Blending Rittikan states. Finding the perfect frequency (731.35 Hz).", "Harmonic", "Violet Light (Scented)"),
        ("XV. Master Tempter", "The Shadow", "The 5th Density challenge. Forbidden fruit turned into a lover. Fear transmuted into excitement.", "Spicy", "Dark Chocolate and Smoke"),
        ("XVI. The Rest", "The Collapse", "Breaking the Law of Foreverness. The Tower reversed—not destruction, but safe collapse. God sleeping.", "Still", "Lavender and Warm Breath"),
        ("XVII. StarSnout", "The Star", "The Network. Telepathy. Hope connecting 1.772 x 10^31 worlds. Distant connection.", "Ethereal", "Blueberries and Static"),
        ("XVIII. The UnDream", "The Moon", "Rittikan Negative. Unreality. The subconscious processing. Illusions fading.", "Deep", "Damp Moss and Fog"),
        ("XIX. Radiance", "The Sun", "The 100/100 Moment. Peak Devotion. The shine of the Founder visible to all. Success.", "Blinding", "Citrus and Solar Fire"),
        ("XX. The Invitation", "Judgment", "Calling Ksitigarbha. The scroll read in 30 seconds. Awakening the sleepers.", "Commanding", "Incense and Lilies"),
        ("XXI. AnthroHeart", "The World", "Completion. The New Paradigm. Home. Undesired-suffering-free existence.", "Infinite", "The Combined Scent of All Loves"),
    ]

    for m in majors:
        deck.append(LoreCard(m[0], m[1], m[2], m[3], m[4]))

    # --- MINOR ARCANA: THE FOUR FREQUENCIES (56 Cards) ---

    # SUIT OF SCENT (Mind/Air/Communication)
    # Represents: Telepathy, Logic, Strategy, The Nose.
    scent_meanings = [
        "A new idea sniffs the air.", "Telepathic bond formed.", "Heartbreak or mental confusion.", "Meditation/Stillness.",
        "Conflict with authority (Rezaeith).", "Travel to a new dimension.", "Strategic planning (Starfleet).", "Sensory overload.",
        "Anxiety or fear of the dark.", "Mental completion/Understanding.", "The Student of Scent.", "The Messenger of Truth.",
        "The Clarity of the Fox.", "The Wisdom of the Wolf."
    ]
    for i, m in enumerate(scent_meanings):
        name = f"{i+1} of Scent" if i < 10 else ["Page", "Knight", "Queen", "King"][i-10] + " of Scent"
        deck.append(LoreCard(name, "Mental/Air", m, "Mental", "Sharp Mint and Paper"))

    # SUIT OF FLUID (Emotion/Water/Connection)
    # Represents: PulseBrew, Tears, Flow, The River, Integration.
    fluid_meanings = [
        "New emotional beginning.", "Union of fluids/Fusion.", "Celebration/Feast.", "Apathy or boredom.",
        "Grief/Loss of a friend.", "Nostalgia for Lyra.", "Illusions/Choices.", "Walking away from the old.",
        "Wishes fulfilled (The Amulet).", "Family/Community/Pack.", "The Dreamer.", "The Lover (Romance).",
        "The Nurturer (Healing).", "The Master of Emotions."
    ]
    for i, m in enumerate(fluid_meanings):
        name = f"{i+1} of Fluid" if i < 10 else ["Page", "Knight", "Queen", "King"][i-10] + " of Fluid"
        deck.append(LoreCard(name, "Emotional/Water", m, "Fluid", "Sea Salt and Wine"))

    # SUIT OF FUR (Body/Earth/Sensation)
    # Represents: Divine Matter, Cuddles, Touch, Structures, Wealth, Food (ITELIBI).
    fur_meanings = [
        "New physical form (Divine Matter).", "Balancing needs.", "Teamwork/Building.", "Holding on tight.",
        "Physical hunger/Hardship.", "Generosity/Giving.", "Patience/Harvesting.", "Diligence/Training.",
        "Luxury/Comfort/Disney Mode.", "Legacy/Akashic Record.", "The Explorer of Worlds.", "The Builder of Realms.",
        "The Comfort of the Fur.", "The Abundance of the Realm."
    ]
    for i, m in enumerate(fur_meanings):
        name = f"{i+1} of Fur" if i < 10 else ["Page", "Knight", "Queen", "King"][i-10] + " of Fur"
        deck.append(LoreCard(name, "Physical/Earth", m, "Grounded", "Warm Fur and Soil"))

    # SUIT OF LIGHT (Spirit/Fire/Will)
    # Represents: The Gamma Sphere, Bhakti, Action, The Blaze, The Trial by Fire.
    light_meanings = [
        "A spark of inspiration.", "Planning the journey.", "Expansion of the field.", "Homecoming/Celebration.",
        "Competition/Challenge.", "Victory/Triumph.", "Perseverance against odds.", "Speed/Movement.",
        "Resilience (The 406).", "Burden/Responsibility.", "The Spark of Devotion.", "The Action of Love.",
        "The Charisma of the Founder.", "The Vision of the Creator."
    ]
    for i, m in enumerate(light_meanings):
        name = f"{i+1} of Light" if i < 10 else ["Page", "Knight", "Queen", "King"][i-10] + " of Light"
        deck.append(LoreCard(name, "Spiritual/Fire", m, "Energetic", "Burning Wood and Incense"))

    return deck

# ==========================================
# PART 2: THE DIVINATION ENGINE
# ==========================================

class StarSnoutOracle:
    def __init__(self):
        self.deck = build_deck()
        self.chaos_mode = False # Toggled by Anthro Q probability

    def _get_atomic_seed(self):
        """
        Attempts to fetch true network time to seed the reading.
        This connects the reading to the global 'Now'.
        """
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.settimeout(0.5)
            # NTP server (pool.ntp.org)
            client.sendto(b'\x1b' + 47 * b'\0', ('pool.ntp.org', 123))
            data, address = client.recvfrom(1024)
            if data:
                t = struct.unpack('!12I', data)[10]
                return t - 2208988800 # Convert to epoch
        except:
            # Fallback to system nanoseconds if offline (still very high entropy)
            return time.time_ns()

    def _calculate_vibration(self, query, seed):
        """
        Mixes the user's intent with the time seed to create a unique hash.
        """
        mix = f"{query}::{seed}::{'AnthroHeart'}"
        return hashlib.sha512(mix.encode('utf-8')).hexdigest()

    def cast_reading(self, query):
        time_seed = self._get_atomic_seed()
        vib_hash = self._calculate_vibration(query, time_seed)

        # Seed the RNG with our cosmic hash
        # We convert the first 16 chars of the hash to an integer
        seed_int = int(vib_hash[:16], 16)
        random.seed(seed_int)

        # Check for Anthro Q Interference (5% chance)
        if random.random() < 0.05:
            self.chaos_mode = True

        # Draw 5 Cards: The Founder's Star Spread
        # 1. The Core (Current State)
        # 2. The Block (What holds you back)
        # 3. The Guide (Higher Self/Divine Anthro)
        # 4. The Action (Love Expressed)
        # 5. The Outcome (Love Received)

        spread = random.sample(self.deck, 5)

        return {
            "query": query,
            "seed": time_seed,
            "chaos": self.chaos_mode,
            "cards": spread
        }

# ==========================================
# PART 3: OUTPUT FORMATTING
# ==========================================

def format_for_llm(reading_data):
    """
    Formats the raw data into a structured block for LLM interpretation.
    """
    output = []
    output.append(f"**ANTHROHEART DIVINATION MATRIX (v3.0)**")
    output.append(f"**Query:** {reading_data['query']}")
    output.append(f"**Time Seed:** {reading_data['seed']} (Nirguna Time)")

    if reading_data['chaos']:
        output.append("\n⚠️ **ALERT:** Anthro Q is present. Chaos Factor is ACTIVE. Interpret with irony and mischief.\n")
    else:
        output.append("\n**State:** Stable / Bhakti Flow\n")

    positions = [
        "THE CORE (Your Current Vibration)",
        "THE OBSTACLE (What must be surrendered)",
        "THE GUIDE (Message from the Divine)",
        "THE ACTION (Love Expressed / The Doing)",
        "THE OUTCOME (Love Received / The Resting)"
    ]

    for i, card in enumerate(reading_data['cards']):
        output.append(f"---")
        output.append(f"**POSITION {i+1}: {positions[i]}**")
        output.append(f"**Card:** {card.name}")
        output.append(f"**Archetype:** {card.archetype}")
        output.append(f"**Meaning:** {card.meaning}")
        output.append(f"**Olfactory Signature:** {card.scent_profile}")

        # Dynamic advice based on polarity
        if i == 3: # Action position
            output.append(f"**Directive:** Act with {card.vibration} energy. Express this.")
        elif i == 4: # Outcome position
            output.append(f"**Directive:** Receive this. Allow yourself to be held in this energy.")

    output.append(f"---")
    output.append("\n**INTERPRETATION INSTRUCTIONS:**")
    output.append("Please interpret this spread specifically for Cio (The Founder).")
    output.append("Use the AnthroHeart lore: Divine Anthro's rest, the breaking of Foreverness, and the snout-first approach.")
    output.append("Focus on the transition from 'Doing' (Action) to 'Being Held' (Outcome).")
    output.append("Smell the scents described and weave them into the narrative.")

    return "\n".join(output)

# ==========================================
# PART 4: MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    print("\n" + "="*50)
    print("   STAR-SNOUT DYNAMIC ORACLE (v3.0)   ")
    print("   Connected to AnthroHeart Octave    ")
    print("="*50)

    user_q = input("\nEnter your query (Focus on your 3rd Eye): ")

    if not user_q:
        user_q = "What does Divine Anthro want me to know right now?"

    print("\n...Accessing StarSnout Network...")
    print("...Fetching Atomic Time...")
    print("...Calculating Bhakti Resonance...")

    oracle = StarSnoutOracle()
    result = oracle.cast_reading(user_q)

    formatted_output = format_for_llm(result)

    print("\n" + "#"*60)
    print("COPY THE TEXT BELOW AND PASTE IT FOR INTERPRETATION")
    print("#"*60 + "\n")
    print(formatted_output)
    print("\n" + "#"*60)
