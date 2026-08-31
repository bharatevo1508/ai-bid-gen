# ai-bid-gen

A Claude Code plugin that helps write bids based on information you provide.

## What it does

1. On setup, it scaffolds a set of directories where you drop the information needed to write a bid (company info, past bids, RFP/tender details, pricing, etc.).
2. It ships skills that read from those directories and generate a tailored bid.

## Status

🚧 Early setup. Directory structure and skills are being finalized.

## Install

Once published to GitHub, add it as a plugin marketplace / plugin in Claude Code.

```
/plugin marketplace add <your-org>/ai-bid-gen
/plugin install ai-bid-gen
```

## Structure

```
ai-bid-gen/
├── .claude-plugin/
│   └── plugin.json        # plugin manifest
├── commands/              # slash commands (e.g. project init, generate bid)
├── skills/                # skills that write bids from provided info
└── README.md
```
