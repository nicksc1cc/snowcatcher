# Snowcatcher — Ski Data Repository

**355 structured data files across 6 countries, 34 domains, 67 resorts, and 246 villages.**

## Structure

```
data/
├── schema.json            Full v3.1 schema (173-question framework, 7 hierarchy levels)
├── france.json             Master hierarchy: regions → domains → resorts → villages
├── countries/              6 country-level research files
│   ├── france.json
│   ├── italy.json
│   ├── switzerland.json
│   ├── austria.json
│   ├── andorra.json
│   └── spain.json
├── domains/                34 domain files
│   ├── les-trois-vallees.json
│   ├── paradiski.json
│   └── ...
├── resorts/                67 resort files
│   ├── val-thorens.json
│   ├── courchevel.json
│   └── ...
└── villages/               246 village/hamlet files
    ├── val-thorens-centre.json
    ├── courchevel-1850.json
    └── ...
```

## Schema hierarchy

```
Country → Region → Domain → Resort → Village → Lift → Piste
```

Every file follows the v3.1 schema. The question_framework section maps all 173 resort questions to their schema fields.

## Coverage

| Level | Files | Content |
|-------|-------|---------|
| Countries | 6 | Ski industry overview, driving laws, winter tyre rules, emergency/mountain rescue, ski insurance, power/currency/language, price positioning vs peers |
| Domains | 34 | Statistics (km, lifts, altitude), lift pass pricing, difficulty split, suitability per audience, signature runs, season dates |
| Resorts | 67 | Altitude, pistes, lifts, character, overview, access, getting around, when to go, beginners, families, off-piste, where to stay, food & drink, après, non-ski activities, services, safety, comparisons |
| Villages | 246 | Specific altitude band data: character, dining (structured restaurants with Michelin stars), shopping, après scene (bars, clubs), activities (15+ types), practical info, lifts, pistes |