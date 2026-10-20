# eco_engine.py
# ─────────────────────────────────────────────────────────────────────────────
# Drop this file next to your app.py. It runs fully independently.
# app.py imports from it — no changes to your Groq setup needed.

# ── Fabric Database ───────────────────────────────────────────────────────────

FABRIC_DB = {
    "organic_cotton": {
        "label": "Organic Cotton",
        "base_eco_score": 82,
        "max_wears": 200,
        "degradation_rate": 0.0015,
        "biodegradable": True,
        "microplastics": False,
        "upcycle_ideas": [
            "Cut into reusable cleaning rags or dish cloths",
            "Make reusable produce bags",
            "Braid into a doormat",
            "Donate to textile recycling programs",
        ],
        "disposal": ["Compost", "Donate", "Textile recycle"],
        "alternatives": ["Linen", "Hemp", "Tencel"],
        "notes": "One of the most sustainable natural fibres when grown organically.",
        "wash_warning": None,
    },
    "cotton": {
        "label": "Cotton",
        "base_eco_score": 55,
        "max_wears": 180,
        "degradation_rate": 0.002,
        "biodegradable": True,
        "microplastics": False,
        "upcycle_ideas": [
            "Turn old T-shirts into tote bags",
            "Cut into reusable makeup wipes",
            "Make quilt patches",
            "Donate to animal shelters as bedding",
        ],
        "disposal": ["Donate", "Upcycle", "Textile recycle"],
        "alternatives": ["Organic Cotton", "Linen", "Tencel"],
        "notes": "Conventional cotton uses significant water and pesticides.",
        "wash_warning": None,
    },
    "linen": {
        "label": "Linen",
        "base_eco_score": 88,
        "max_wears": 250,
        "degradation_rate": 0.001,
        "biodegradable": True,
        "microplastics": False,
        "upcycle_ideas": [
            "Make linen napkins or placemats",
            "Create bread bags",
            "Use as plant ties in the garden",
            "Compost at end of life",
        ],
        "disposal": ["Compost", "Donate", "Textile recycle"],
        "alternatives": [],
        "notes": "Highly durable, naturally pest-resistant, and fully biodegradable.",
        "wash_warning": None,
    },
    "hemp": {
        "label": "Hemp",
        "base_eco_score": 92,
        "max_wears": 300,
        "degradation_rate": 0.0008,
        "biodegradable": True,
        "microplastics": False,
        "upcycle_ideas": [
            "Compost directly — breaks down quickly",
            "Use as natural rope or twine",
            "Cut into seed-starting pots for the garden",
        ],
        "disposal": ["Compost", "Donate", "Upcycle"],
        "alternatives": [],
        "notes": "One of the most sustainable fibres — sequesters carbon and improves soil.",
        "wash_warning": None,
    },
    "wool": {
        "label": "Wool",
        "base_eco_score": 70,
        "max_wears": 300,
        "degradation_rate": 0.001,
        "biodegradable": True,
        "microplastics": False,
        "upcycle_ideas": [
            "Felt old woollen jumpers into bags or hats",
            "Unravel and reuse as yarn",
            "Use as garden mulch — wool retains moisture",
            "Stuff cushions or pet beds",
        ],
        "disposal": ["Compost", "Donate", "Textile recycle"],
        "alternatives": ["Organic Cotton", "Linen"],
        "notes": "Natural and biodegradable but sheep farming has a methane footprint.",
        "wash_warning": None,
    },
    "silk": {
        "label": "Silk",
        "base_eco_score": 60,
        "max_wears": 150,
        "degradation_rate": 0.003,
        "biodegradable": True,
        "microplastics": False,
        "upcycle_ideas": [
            "Make hair scrunchies or sleep masks",
            "Use as cleaning cloths for lenses",
            "Create a patchwork art piece",
            "Donate to vintage textile collectors",
        ],
        "disposal": ["Donate", "Upcycle", "Textile recycle"],
        "alternatives": ["Tencel"],
        "notes": "Biodegradable but energy-intensive to produce. Handle with care.",
        "wash_warning": None,
    },
    "tencel": {
        "label": "Tencel",
        "base_eco_score": 85,
        "max_wears": 200,
        "degradation_rate": 0.0012,
        "biodegradable": True,
        "microplastics": False,
        "upcycle_ideas": [
            "Use as soft cleaning cloths",
            "Cut into reusable face wipes",
            "Compost at end of life",
        ],
        "disposal": ["Compost", "Donate", "Upcycle"],
        "alternatives": [],
        "notes": "Made in a closed-loop process — solvent is recaptured and reused.",
        "wash_warning": None,
    },
    "bamboo": {
        "label": "Bamboo",
        "base_eco_score": 68,
        "max_wears": 160,
        "degradation_rate": 0.002,
        "biodegradable": True,
        "microplastics": False,
        "upcycle_ideas": [
            "Cut into soft face cloths",
            "Compost at end of life",
            "Use as gentle dusting cloths",
        ],
        "disposal": ["Compost", "Donate", "Upcycle"],
        "alternatives": ["Tencel", "Organic Cotton"],
        "notes": "Plant is sustainable but chemical-heavy processing reduces overall score.",
        "wash_warning": None,
    },
    "polyester": {
        "label": "Polyester",
        "base_eco_score": 28,
        "max_wears": 200,
        "degradation_rate": 0.0005,
        "biodegradable": False,
        "microplastics": True,
        "upcycle_ideas": [
            "Donate to fast-fashion take-back schemes (H&M, Zara, etc.)",
            "Use as padding inside a draught stopper",
            "Cut into microfibre cleaning cloths",
            "Check local textile recycling for synthetic fibres",
        ],
        "disposal": ["Synthetic recycle", "Donate"],
        "alternatives": ["Tencel", "Recycled Polyester", "Organic Cotton"],
        "notes": "Sheds microplastics with every wash. Never compost. Maximise wears.",
        "wash_warning": "Use a GuppyFriend bag or Cora Ball to catch microplastics when washing.",
    },
    "recycled_polyester": {
        "label": "Recycled Polyester",
        "base_eco_score": 52,
        "max_wears": 200,
        "degradation_rate": 0.0005,
        "biodegradable": False,
        "microplastics": True,
        "upcycle_ideas": [
            "Return to brand take-back schemes",
            "Donate to specialist rPET recyclers",
        ],
        "disposal": ["Synthetic recycle", "Donate"],
        "alternatives": ["Tencel", "Organic Cotton"],
        "notes": "Better than virgin polyester — uses ~50% less energy — but still sheds microplastics.",
        "wash_warning": "Use a microplastic filter bag when washing.",
    },
    "nylon": {
        "label": "Nylon",
        "base_eco_score": 22,
        "max_wears": 250,
        "degradation_rate": 0.0004,
        "biodegradable": False,
        "microplastics": True,
        "upcycle_ideas": [
            "Look for Terracycle drop-off points",
            "Repurpose tights as plant ties in the garden",
            "Use as mesh bags for produce",
        ],
        "disposal": ["Synthetic recycle", "Donate"],
        "alternatives": ["Recycled Nylon", "Tencel"],
        "notes": "Nylon production emits N₂O, a potent greenhouse gas. Wear as long as possible.",
        "wash_warning": "Use a microplastic filter bag when washing.",
    },
    "acrylic": {
        "label": "Acrylic",
        "base_eco_score": 15,
        "max_wears": 80,
        "degradation_rate": 0.006,
        "biodegradable": False,
        "microplastics": True,
        "upcycle_ideas": [
            "Donate while still wearable — avoid landfill",
            "Repurpose as stuffing for draught excluders",
            "Use as a pet blanket before disposal",
        ],
        "disposal": ["Donate"],
        "alternatives": ["Organic Cotton", "Wool", "Tencel"],
        "notes": "Sheds the most microplastics of any fibre. One of the least sustainable choices.",
        "wash_warning": "Sheds very high levels of microplastics — always use a filter bag.",
    },
    "spandex": {
        "label": "Spandex / Elastane",
        "base_eco_score": 18,
        "max_wears": 100,
        "degradation_rate": 0.004,
        "biodegradable": False,
        "microplastics": True,
        "upcycle_ideas": [
            "Return to athletic brand take-back schemes",
            "Repurpose as resistance bands",
            "Use as cable ties or organisers",
        ],
        "disposal": ["Donate"],
        "alternatives": ["Recycled Polyester"],
        "notes": "Nearly impossible to recycle due to stretch fibres. Wear as long as possible.",
        "wash_warning": "Use a microplastic filter bag when washing.",
    },
    "elastane": {
        "label": "Elastane",
        "base_eco_score": 18,
        "max_wears": 100,
        "degradation_rate": 0.004,
        "biodegradable": False,
        "microplastics": True,
        "upcycle_ideas": [
            "Return to athletic brand take-back schemes",
            "Use as cable ties or organisers",
        ],
        "disposal": ["Donate"],
        "alternatives": ["Recycled Polyester"],
        "notes": "Nearly impossible to recycle. Wear as long as possible.",
        "wash_warning": "Use a microplastic filter bag when washing.",
    },
    "viscose": {
        "label": "Viscose / Rayon",
        "base_eco_score": 40,
        "max_wears": 120,
        "degradation_rate": 0.003,
        "biodegradable": True,
        "microplastics": False,
        "upcycle_ideas": [
            "Compost at end of life (if no synthetic blends)",
            "Use as soft lining material in upcycled bags",
            "Repurpose as a cleaning cloth",
        ],
        "disposal": ["Compost", "Donate", "Upcycle"],
        "alternatives": ["Tencel", "Organic Cotton"],
        "notes": "Plant-based but chemically processed. Tencel is a better closed-loop alternative.",
        "wash_warning": None,
    },
    "rayon": {
        "label": "Rayon",
        "base_eco_score": 40,
        "max_wears": 120,
        "degradation_rate": 0.003,
        "biodegradable": True,
        "microplastics": False,
        "upcycle_ideas": [
            "Compost at end of life",
            "Use as cleaning cloths",
            "Donate to textile banks",
        ],
        "disposal": ["Compost", "Donate"],
        "alternatives": ["Tencel", "Organic Cotton"],
        "notes": "Same as viscose — plant-based but chemical processing lowers its score.",
        "wash_warning": None,
    },
    "denim": {
        "label": "Denim",
        "base_eco_score": 45,
        "max_wears": 300,
        "degradation_rate": 0.001,
        "biodegradable": True,
        "microplastics": False,
        "upcycle_ideas": [
            "Cut into shorts or a skirt",
            "Make a denim tote or backpack",
            "Use as patching material for other jeans",
            "Donate to denim recycling (Levi's, Nudie Jeans, etc.)",
        ],
        "disposal": ["Donate", "Upcycle", "Textile recycle"],
        "alternatives": ["Organic Cotton Denim"],
        "notes": "Extremely water-intensive to produce. Denim is incredibly upcyclable.",
        "wash_warning": None,
    },
    "leather": {
        "label": "Leather",
        "base_eco_score": 30,
        "max_wears": 500,
        "degradation_rate": 0.0003,
        "biodegradable": False,
        "microplastics": False,
        "upcycle_ideas": [
            "Repair with leather conditioner to extend life significantly",
            "Use scraps for small accessories like keyrings",
            "Take to a cobbler for resoling rather than replacing",
            "Donate to leather craft communities",
        ],
        "disposal": ["Donate", "Upcycle", "Specialist recycle"],
        "alternatives": ["Cork Leather", "Mushroom Leather"],
        "notes": "Very high production impact, but extremely long lifespan. Maintain well.",
        "wash_warning": None,
    },
    "cashmere": {
        "label": "Cashmere",
        "base_eco_score": 58,
        "max_wears": 200,
        "degradation_rate": 0.002,
        "biodegradable": True,
        "microplastics": False,
        "upcycle_ideas": [
            "Unravel and reuse as luxury yarn",
            "Felt into accessories",
            "Donate to premium clothing banks",
        ],
        "disposal": ["Compost", "Donate", "Upcycle"],
        "alternatives": ["Organic Cotton", "Wool"],
        "notes": "Biodegradable but cashmere goats cause significant land degradation.",
        "wash_warning": None,
    },
    "fleece": {
        "label": "Fleece",
        "base_eco_score": 20,
        "max_wears": 150,
        "degradation_rate": 0.003,
        "biodegradable": False,
        "microplastics": True,
        "upcycle_ideas": [
            "Donate to animal shelters as bedding",
            "Use as padding inside cushions",
            "Cut into cleaning cloths",
        ],
        "disposal": ["Donate", "Synthetic recycle"],
        "alternatives": ["Recycled Fleece", "Wool"],
        "notes": "Sheds significant microplastics. Look for recycled fleece alternatives.",
        "wash_warning": "One of the highest microplastic shedders — always use a filter bag.",
    },
}

# ── Fabric matcher ────────────────────────────────────────────────────────────

def match_fabric(label: str) -> str | None:
    """
    Maps a raw label from Groq (e.g. 'cotton, polyester') to a DB key.
    Returns None if unrecognised.
    """
    label = label.lower().strip()
    if "organic cotton" in label:       return "organic_cotton"
    if "recycled polyester" in label:   return "recycled_polyester"
    if "tencel" in label or "lyocell" in label: return "tencel"
    if "bamboo" in label:               return "bamboo"
    if "hemp" in label:                 return "hemp"
    if "linen" in label or "flax" in label: return "linen"
    if "silk" in label:                 return "silk"
    if "cashmere" in label:             return "cashmere"
    if "wool" in label or "merino" in label: return "wool"
    if "fleece" in label:               return "fleece"
    if "polyester" in label:            return "polyester"
    if "nylon" in label or "polyamide" in label: return "nylon"
    if "acrylic" in label:              return "acrylic"
    if "spandex" in label or "lycra" in label: return "spandex"
    if "elastane" in label:             return "elastane"
    if "viscose" in label:              return "viscose"
    if "rayon" in label:                return "rayon"
    if "denim" in label:                return "denim"
    if "leather" in label:              return "leather"
    if "cotton" in label:               return "cotton"
    return None

# ── Scoring logic ─────────────────────────────────────────────────────────────

ECO_ALERT_THRESHOLD = 35   # score below this = trigger upcycle advice
WEAR_ALERT_RATIO    = 0.70  # 70% of max wears = "worn a lot"

def calc_eco_score(fabric: dict, wears: int) -> float:
    raw = fabric["base_eco_score"] * (1 - fabric["degradation_rate"] * wears)
    return round(max(0.0, min(100.0, raw)), 1)

def calc_wears_remaining(fabric: dict, wears: int) -> int:
    until_eol = max(0, fabric["max_wears"] - wears)
    base = fabric["base_eco_score"]
    if base <= ECO_ALERT_THRESHOLD:
        return until_eol
    wears_at_threshold = (1 - ECO_ALERT_THRESHOLD / base) / fabric["degradation_rate"]
    until_threshold = max(0, int(wears_at_threshold - wears))
    return min(until_eol, until_threshold)

def get_eco_tier(score: float) -> dict:
    if score >= 75: return {"tier": "excellent", "label": "Excellent", "emoji": "🌿", "colour": "#4CAF50"}
    if score >= 55: return {"tier": "good",      "label": "Good",      "emoji": "🍃", "colour": "#8BC34A"}
    if score >= 35: return {"tier": "moderate",  "label": "Moderate",  "emoji": "🌱", "colour": "#FFC107"}
    if score >= 15: return {"tier": "poor",      "label": "Poor",      "emoji": "⚠️", "colour": "#FF5722"}
    return             {"tier": "critical",  "label": "Critical",  "emoji": "🔴", "colour": "#F44336"}

def build_advice(fabric: dict, wears: int, score: float, wears_remaining: int) -> dict:
    wear_ratio = wears / fabric["max_wears"]
    high_wears = wear_ratio >= WEAR_ALERT_RATIO
    low_score  = score < ECO_ALERT_THRESHOLD

    if high_wears and low_score:
        urgency = "now"
        message = (
            f"This garment has been worn {wears} times and its eco impact is now significant. "
            f"It's the right time to give it a second life rather than sending it to landfill."
        )
    elif high_wears:
        urgency = "soon"
        message = (
            f"Great use of this piece! It has around {wears_remaining} wears left. "
            f"Start thinking about its next chapter."
        )
    elif low_score:
        urgency = "soon"
        message = (
            f"The environmental impact of this fabric is notable. "
            f"Consider its future when you have {wears_remaining} wears remaining."
        )
    elif wear_ratio >= 0.50:
        urgency = "consider"
        message = (
            f"You're halfway through this garment's lifespan — great progress! "
            f"Keep wearing it to reduce its per-use footprint."
        )
    else:
        urgency = "none"
        message = "Keep wearing! Every additional wear lowers the per-wear environmental cost."

    return {
        "urgency": urgency,
        "should_upcycle": urgency in ("now", "soon"),
        "message": message,
        "upcycle_ideas": fabric["upcycle_ideas"],
        "disposal": fabric["disposal"],
        "alternatives": fabric["alternatives"],
        "wash_warning": fabric.get("wash_warning"),
    }

# ── Main entry point ──────────────────────────────────────────────────────────

def analyse_garment(detected_label: str, wear_count: int = 0) -> dict:
    """
    Full eco analysis for a garment.

    Args:
        detected_label: raw fabric string from Groq (e.g. "cotton" or "cotton, polyester")
        wear_count:     how many times this garment has been worn (default 0)

    Returns:
        dict with full eco analysis, ready to pass to your Jinja template.
    """
    # Handle blends — split on comma, analyse each, weighted average
    parts = [p.strip() for p in detected_label.split(",") if p.strip()]

    matched = []
    for part in parts:
        key = match_fabric(part)
        if key and key in FABRIC_DB:
            matched.append((part, FABRIC_DB[key]))

    if not matched:
        return {
            "success": False,
            "error": f"Fabric '{detected_label}' not yet in our database.",
            "detected_label": detected_label,
        }

    # Weighted average eco score (equal weight per fabric if blend)
    weight = 1 / len(matched)
    blended_base = sum(f["base_eco_score"] * weight for _, f in matched)
    blended_deg  = sum(f["degradation_rate"] * weight for _, f in matched)
    blended_max  = int(sum(f["max_wears"] * weight for _, f in matched))

    # Synthetic blend proxy for advice
    primary_label, primary_fabric = matched[0]

    # Build a synthetic fabric entry for blends
    proxy = {
        **primary_fabric,
        "base_eco_score": blended_base,
        "degradation_rate": blended_deg,
        "max_wears": blended_max,
        "biodegradable": all(f["biodegradable"] for _, f in matched),
        "microplastics": any(f["microplastics"] for _, f in matched),
    }

    score          = calc_eco_score(proxy, wear_count)
    wears_rem      = calc_wears_remaining(proxy, wear_count)
    tier           = get_eco_tier(score)
    advice         = build_advice(proxy, wear_count, score, wears_rem)
    wear_pct       = round((wear_count / proxy["max_wears"]) * 100)

    is_blend = len(matched) > 1

    return {
        "success":        True,
        "detected_label": detected_label,
        "fabric_label":   " + ".join(f["label"] for _, f in matched),
        "is_blend":       is_blend,
        "eco_score":      score,
        "base_eco_score": round(blended_base, 1),
        "eco_tier":       tier,
        "wear_count":     wear_count,
        "wears_remaining": wears_rem,
        "max_wears":      proxy["max_wears"],
        "wear_pct_used":  wear_pct,
        "biodegradable":  proxy["biodegradable"],
        "microplastics":  proxy["microplastics"],
        "notes":          primary_fabric["notes"],
        "advice":         advice,
    }
