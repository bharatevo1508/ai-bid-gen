---
description: Scaffold the bid-resources knowledge base (case studies, projects, sample bids, profiles)
---

You are initializing the **bid-resources** knowledge base for the ai-bid-gen plugin.

Create the following directory structure in the current working directory. If a folder or file already exists, **do not overwrite it** — leave the user's content intact and only create what is missing.

```
bid-resources/
├── case-studies/
│   ├── README.md
│   └── _template.md
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

### bid-resources/case-studies/README.md
```md
# Case Studies

One file per case study. These are matched to a job by **problem type** — when a
job describes a problem you've already solved, the matching case study is pulled
into the bid as proof.

Copy `_template.md` to a new file (e.g. `realtime-chat-scaling.md`) and fill it in.
```

### bid-resources/case-studies/_template.md
```md
# <Case study title>

## Problem
<The problem the client faced. Be specific about the pain / challenge.>

## Solution
<What you did to solve it. Approach, key decisions.>

## Tech used
<Languages, frameworks, services.>

## Outcome / Results
<Measurable results — %, time saved, revenue, scale, uptime, etc.>

## Link
<Optional: live URL, repo, or reference.>
```

### bid-resources/projects/README.md
```md
# Projects

One file per project. These establish **credibility and tech match** — when a
job's tech stack overlaps with a project, it's cited to show you've shipped this
kind of work, ideally with a live URL.

Copy `_template.md` to a new file (e.g. `acme-dashboard.md`) and fill it in.
```

### bid-resources/projects/_template.md
```md
# <Project name>

## Overview
<What the project is, in 2-4 sentences.>

## Responsibilities
<What you / your team were responsible for.>

## Tech stack
<Languages, frameworks, infra, databases, services.>

## Production URLs
<Live links to the deployed product.>
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

Copy `_template.md` to a new file (e.g. `senior-fullstack.md`) and fill it in.
```

### bid-resources/profiles/_template.md
```md
# <Profile name / persona>

## Profile URL
<Link to the Upwork profile.>

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

Report back a summary of what was created (and what already existed and was skipped), then tell the user to populate the folders with their real content and run the bid generation skill when ready.
