---
description: Scaffold the bid-resources knowledge base (projects, sample bids, profiles)
---

You are initializing the **bid-resources** knowledge base for the ai-bid-gen plugin.

Create the following directory structure in the current working directory. If a folder or file already exists, **do not overwrite it** — leave the user's content intact and only create what is missing.

```
bid-resources/
├── projects/
│   ├── README.md
│   └── _template.md
├── sample-bids/
│   ├── README.md
│   └── _template.md
└── profiles/
    ├── README.md
    └── _template.md
```

## File contents

### bid-resources/projects/README.md
```md
# Projects

One file per project. Each project is **both** a credibility signal *and* a case
study — it establishes tech match (what you've shipped, ideally with a live URL)
and tells the story of the problem you solved and the outcome you drove.

A project is matched to a job on **either axis**:
- by **problem type** — when a job describes a problem this project solved, and
- by **tech stack** — when a job's stack overlaps with this project's.

Fill in as much as you have. A rich project fills every section (problem +
outcome + live URL). A breadth-only portfolio entry can leave **Problem** and
**Outcome / Results** empty and just carry the overview, tech stack, and URL.

Copy `_template.md` to a new file (e.g. `acme-dashboard.md`) and fill it in.
Just write the prose — you do **not** need to add any structured frontmatter by
hand. After adding or editing projects, run `/ai-bid-gen:organize-kb`; it reads
your prose, adds the frontmatter used for fast retrieval, and builds an index.
```

### bid-resources/projects/_template.md
```md
# <Project name>

## Overview
<What the project is, in 2-4 sentences.>

## Problem
<The problem the client / business faced. Be specific about the pain / challenge.
Leave empty for a breadth-only portfolio entry.>

## Solution / Responsibilities
<What you did to solve it — approach, key decisions, what you were responsible for.>

## Tech stack
<Languages, frameworks, infra, databases, services.>

## Outcome / Results
<Measurable results — %, time saved, revenue, scale, uptime, etc. Leave empty if
you don't have a measured outcome for this one.>

## Production URLs
<Live links to the deployed product. Optional.>
```

### bid-resources/sample-bids/README.md
```md
# Sample Bids

Bids that were already submitted **and accepted**. These teach the generator your
winning structure, tone, length, and opening hooks. The more you add, the better
the generated bids match what actually wins for you.

Copy `_template.md` to a new file (e.g. `won-saas-mvp.md`) and paste the bid.
```

### bid-resources/sample-bids/_template.md
```md
# <Short label for this won bid>

## Job context (optional)
<A sentence or two about the job this bid won — type of client / project.>

## Bid text
<Paste the exact bid text that was submitted and accepted.>
```

### bid-resources/profiles/README.md
```md
# Profiles

One file per Upwork profile. A bid is written **as** a specific profile — using
its voice, its advertised skills, and its hourly rate for any pricing. Pick which
profile you're bidding as when generating a bid.

Two fields are easy to skip and worth filling in: **GitHub / website**, because
posts regularly demand a link and a missing one gets the application filtered out,
and **Portfolio items**, which lists the projects already published on this Upwork
profile so a bid can tell you what to attach.

Copy `_template.md` to a new file (e.g. `senior-fullstack.md`) and fill it in.
```

### bid-resources/profiles/_template.md
```md
# <Profile name / persona>

## Profile URL
<Link to the Upwork profile.>

## GitHub / website
<GitHub profile URL, plus any personal site or portfolio. Leave as-is if there is none.>

## Portfolio items
<An array of strings: the projects already published as portfolio pieces on THIS Upwork
profile, so a bid can tell you what to attach. Each string is the name of a file in
bid-resources/projects/ without the .md — the names must match that folder exactly.
Use [] if this profile has no portfolio pieces. e.g. ["realtime-sync", "ops-dashboard"]>
[]

## Title / headline
<The profile's headline.>

## Introduction
<The intro / summary paragraph, in the voice this profile uses.>

## Description
<Longer description of skills, experience, positioning.>

## Hourly rate
<e.g. $45/hr>

## Skills
<Comma-separated key skills.>

## Notes
<Anything else useful — availability, specialties, preferred project types.>
```

## After creating

Report back a summary of what was created (and what already existed and was skipped), then tell the user to populate the folders with their real content. Once projects are added, they should run `/ai-bid-gen:organize-kb` to structure the knowledge base for retrieval, then run the bid generation skill when ready.
