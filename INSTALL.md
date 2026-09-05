# Install Lumiverse Toolkit

Lumiverse Toolkit v0.2 bundles five skills. It has no MCP server, external account connection, or hooks. Python 3.10+ is required for bundled validators and CHARX packaging; Node.js is required for the preset Regex checker. Both specialists are included without a separate personal-skill installation.

## Install from the GitHub marketplace

### Codex CLI

1. Add the marketplace:

   ```bash
   codex plugin marketplace add drinkwaterdrink/Lumiverse---Toolkit
   ```

2. Open the plugin browser:

   ```text
   /plugins
   ```

3. Select the **Lumiverse Toolkit** marketplace, open **lumiverse-toolkit**, and install it.
4. Start a new session before using its bundled skills.

### ChatGPT desktop app

1. Clone or download this repository and open it as a local project.
2. Restart the ChatGPT desktop app so it discovers `.agents/plugins/marketplace.json`.
3. Open **Plugins**, select **Lumiverse Toolkit**, and install **lumiverse-toolkit**.
4. Start a new Chat or Work conversation.

## Use it

Describe the outcome directly and allow automatic routing, or type `@` in ChatGPT and select a bundled skill.

Starter prompts:

- `@Lumiverse Project Steward Start a reusable Lumiverse project from this material. Track canon, artifacts, dependencies, blockers, and validation.`
- `@Lumiverse Character Forge Create a rich Lumiverse character package. Treat my statements as canon, keep generated additions provisional, and protect {{user}} agency.`
- `@Lumiverse Scenario Forge Turn this premise into a RICH SANDBOX scenario seed with an open first moment and no predetermined user feelings or decisions.`

World Book work routes to **Forge Lumiverse Lorebooks** and SillyTavern Chat Completion preset conversion routes to **Lumiverse Preset Converter** when those specialist skills are available.

## Android/mobile note

ChatGPT mobile can use plugins and bundled skills that are available to your account. A GitHub marketplace is the development and private-distribution source; it does not by itself publish the plugin to OpenAI's universal Plugins Directory. Direct directory installation on Android requires a later OpenAI plugin submission and approval.

## Update or roll back

- Run `codex plugin marketplace upgrade lumiverse-toolkit-marketplace` to refresh the marketplace snapshot, then reinstall or update the plugin in `/plugins`.
- For a rollback, install from a tagged release or Git commit instead of `main`.
- Export any active project record before changing versions so stable IDs, canon status, and unresolved items remain recoverable.
