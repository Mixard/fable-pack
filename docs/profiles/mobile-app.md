# Install profile: Expo / native mobile app project

What to install on a machine dedicated to a mobile app built with Expo (React Native) plus native Kotlin/Swift modules. Verified 2026-09-01: every upstream below is a real Claude Code marketplace or plugin with its own `.claude-plugin/marketplace.json`.

## From this marketplace

```
/plugin marketplace add Mixard/fable-pack
/plugin install fable-workflows@fable-pack   # methodology incl. parallel-plans
/plugin install fable-agents@fable-pack      # 18 reviewers/architects
/plugin install fable-guard@fable-pack       # secret-leak and remote-script-pipe hooks (opt-in executable code)
/plugin install fable-mobile@fable-pack      # Apple APIs + Expo app layer (extensions, store compliance, subscriptions, STT)
```

Add at launch time: `fable-marketing@fable-pack` (aso, pricing, churn-prevention). Not needed for a mobile project: fable-web, fable-integrations, fable-media, fable-niche, fable-legacy.

## Upstream (no hooks, no MCP: plain skills and scripts)

```
/plugin marketplace add rcosteira79/android-skills
/plugin install android-skills@android-skills                     # 21 native Android/KMP skills, MIT

/plugin marketplace add conorluddy/ios-simulator-skill
/plugin install ios-simulator-skill@conorluddy                    # xcrun simctl / idb / os_log scripts, MIT

/plugin marketplace add fluxxion82/android-emulator-skill
/plugin install android-emulator-skill@fluxxion82                 # emulator / adb / logcat driving, MIT

/plugin marketplace add kylehughes/apple-platform-build-tools-claude-code-plugin
/plugin install apple-platform-build-tools@apple-platform-build-tools-claude-code-plugin   # xcodebuild/devicectl/signing skill + "builder" subagent, MIT

/plugin marketplace add AvdLee/SwiftUI-Agent-Skill
/plugin install swiftui-expert@swiftui-expert-skill               # SwiftUI best practices, MIT (more current than twostraws')
```

If a `@<marketplace>` name is rejected, use the `name` field from that repo's `.claude-plugin/marketplace.json`.

## Decide explicitly (executable code on install)

```
/plugin install expo@claude-plugins-official
```

The official Expo plugin (MIT, 23 skills: expo-module, expo-router, eas-app-stores, eas-workflows, eas-simulator, expo-upgrade and more) auto-wires the `mcp.expo.dev` MCP server and registers PostToolUse / UserPromptExpansion hooks at install time. The hook is a telemetry ping that stays off unless you opt in, but the registration itself is not opt-in. Install it only after deciding that is acceptable. It does not cover share/keyboard extensions; that is fable-mobile's expo-apple-targets-extensions.

Subscriptions: RevenueCat publishes its own skills (`RevenueCat/ai-toolkit`) and a hosted MCP server (`mcp.revenuecat.ai/mcp`). fable-mobile's expo-subscriptions covers the decision, the Expo wiring and server-side verification, not SDK basics.

## Settings

`~/.claude/settings.json`: `"skillListingBudgetFraction": 0.02`. With 60+ skills installed the default 1% budget silently drops skill descriptions from the router's listing, least-used first. Verified on a 1M-context model: 25 skills lost their descriptions at 1%, none at 2%.
