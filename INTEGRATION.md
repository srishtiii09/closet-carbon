# Closet Carbon — Integration Guide

## What was already done ✅
- Upload outfit image
- AI fabric detection → returns label (e.g. "100% Polyester")
- Static eco points display

## What these new files add ✅
- **Contextual eco score** — score changes as wear count increases
- **Wears remaining** — estimated wears before environmental impact becomes significant
- **Wear tracker** — log wears per garment over time
- **Upcycle/thrift trigger** — auto-suggests alternatives after high wears + low score
- **Disposal guidance** — what to do with each fabric type at end of life
- **Alternatives engine** — suggests greener fabric swaps
- **REST API** — ready for your Figma frontend to call

---

## New Files

```
closet-carbon/
├── data/
│   └── fabricDatabase.js      ← All fabric eco data (add fabrics here)
├── logic/
│   ├── ecoEngine.js           ← Core eco score calculations
│   └── wearTracker.js         ← Per-garment wear tracking (swap in your DB)
└── api/
    ├── routes.js              ← Express routes (mount in your app)
    └── closetCarbonClient.js  ← Frontend JS client (copy to your frontend)
```

---

## Step 1 — Mount the API routes in your existing Express app

In your main `app.js` or `server.js`, add:

```js
const closetRoutes = require('./api/routes');
app.use('/api/closet', closetRoutes);
```

That's it. Your existing routes are untouched.

---

## Step 2 — Connect your existing fabric detector to the new engine

After your AI returns a fabric label, instead of just displaying the static score, call:

```js
const { analyseGarment } = require('./logic/ecoEngine');

// Your AI already gives you this:
const detectedLabel = "100% Polyester"; // from your existing detector

// Now get the full contextual analysis:
const result = analyseGarment(detectedLabel, 0); // 0 = brand new

// result now contains:
result.ecoScore          // contextual score (e.g. 28)
result.wearsRemaining    // (e.g. 120)
result.ecoTier           // { tier: 'poor', label: 'Poor', emoji: '⚠️' }
result.advice.message    // friendly message for the user
result.advice.upcycleIdeas   // array of upcycle suggestions
result.advice.shouldUpcycle  // true/false
result.biodegradable     // true/false
result.microplastics     // true/false
```

---

## Step 3 — Connect your database to the wear tracker

Open `logic/wearTracker.js` and find the three functions marked `// TODO`:

```js
async function _getGarment(id) {
  // TODO: replace with → await YourDB.findById(id)
  return _store[id] || null;
}

async function _saveGarment(garment) {
  // TODO: replace with → await YourDB.save(garment)
  _store[garment.id] = garment;
  return garment;
}

async function _getAllGarments() {
  // TODO: replace with → await YourDB.findAll()
  return Object.values(_store);
}
```

Replace the `_store` mock with your actual DB calls (MongoDB, Supabase, Firebase, etc.)
Each garment document needs these fields:
```js
{
  id: String,
  name: String,
  fabricLabel: String,
  blendData: Array | null,
  imageUrl: String | null,
  wearCount: Number,
  addedAt: String (ISO date),
  lastWorn: String | null (ISO date)
}
```

---

## Step 4 — Link your Figma frontend

### Option A: Figma Prototype with API calls (recommended)

1. Copy `api/closetCarbonClient.js` into your frontend project (React/Vue/Next etc.)
2. Set the base URL in the file:
   ```js
   const BASE_URL = 'http://localhost:3001/api/closet'; // dev
   // or your deployed URL in production
   ```
3. Import and use in your components:
   ```js
   import { analyseInstant, logWear, getWardrobe } from './closetCarbonClient';

   // Right after your AI detects the fabric:
   const eco = await analyseInstant(detectedFabricLabel);

   // When user taps "I wore this today":
   const updated = await logWear(garmentId);
   if (updated.alert) showUpcycleBanner(updated.alert.message);

   // For wardrobe overview screen:
   const wardrobe = await getWardrobe();
   ```

### Option B: Figma Plugin

If you're building a Figma Plugin (not a web prototype):
1. Figma plugins can make `fetch()` calls but need `"networkAccess"` in `manifest.json`:
   ```json
   {
     "networkAccess": {
       "allowedDomains": ["http://localhost:3001", "https://your-api.com"]
     }
   }
   ```
2. Use the same `closetCarbonClient.js` functions inside your plugin's `ui.html`.

### Option C: Figma + Framer / Webflow

If your Figma designs are exported to Framer or Webflow:
- Framer: paste the client functions into a Framer Code Component
- Webflow: include the client as a `<script>` and call functions from Webflow interactions

---

## Step 5 — Data flow for each Figma screen

### Screen: Upload & Detect
```
User uploads image
  → Your existing AI detects fabric
  → Call: analyseInstant(fabricLabel)
  → Display: ecoScore, ecoTier.emoji, wearsRemaining, advice.message
  → If user saves: call addGarment(...)
```

### Screen: Garment Detail
```
Load: getGarment(garmentId)
  → Show: ecoScore progress bar (use ecoScoreColour(score) helper)
  → Show: wearCount / maxWears
  → Show: wearsRemaining label (use formatWearsRemaining() helper)
  → Show: advice.upcycleIdeas (if advice.shouldUpcycle)
  → Button "I wore this": logWear(garmentId)
```

### Screen: Wardrobe Overview
```
Load: getWardrobe()
  → Sort is automatic (urgent items first)
  → Each card shows: ecoTier.emoji + ecoScore + urgency CTA
  → Use getCtaLabel(urgency) for button text
```

### Screen: Upcycle / Retire
```
User chooses disposal method
  → Call: retireGarment(garmentId, "donated" | "upcycled" | etc.)
  → Show final summary + eco impact summary
```

---

## API Reference (quick)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/closet/analyse` | Instant analysis (no storage) |
| POST | `/api/closet/garments` | Add garment to wardrobe |
| GET  | `/api/closet/garments` | Full wardrobe (sorted by urgency) |
| GET  | `/api/closet/garments/:id` | Single garment analysis |
| POST | `/api/closet/garments/:id/wear` | Log a wear |
| POST | `/api/closet/garments/:id/retire` | Retire (donate/upcycle/etc.) |
| GET  | `/api/closet/fabrics` | All fabrics in database |

---

## Adding new fabrics

Open `data/fabricDatabase.js` and add an entry following this template:

```js
my_fabric: {
  label: "My Fabric",
  baseEcoScore: 70,        // 0–100, new garment
  maxWears: 200,           // estimated full lifespan
  degradationRate: 0.0015, // eco score lost per wear (fraction of base)
  biodegradable: true,
  microplastics: false,
  co2PerKg: 5,
  waterLitresPerKg: 800,
  disposalOptions: ["compost", "donate"],
  upcycleIdeas: ["idea 1", "idea 2"],
  alternatives: ["tencel", "linen"],
  notes: "Brief summary for the user."
}
```

Then add a match rule in the `matchFabric()` function in the same file:
```js
if (label.includes("my fabric")) return "my_fabric";
```
