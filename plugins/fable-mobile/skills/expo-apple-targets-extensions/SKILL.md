---
name: expo-apple-targets-extensions
description: Use when adding an iOS share extension or custom keyboard extension to an Expo/React Native app via @bacons/apple-targets (expo-apple-targets, by Evan Bacon). Covers expo-target.config.js schema, App Groups data hand-off, EAS Build signing, share-extension activation rules and memory limits, keyboard RequestsOpenAccess constraints, and known prebuild bugs.
---

# iOS share/keyboard extensions in Expo via expo-apple-targets

Package `@bacons/apple-targets` (repo `EvanBacon/expo-apple-targets`), latest `5.0.0` (published 2026-07-17). Companion CLI package `create-target` (unscoped), latest `3.0.5`. `peerDependencies.expo` is `>=52`, but the README's prose states "+53" as the practical minimum — unreconciled, treat 53 as the safer floor. README also states: CocoaPods >=1.16.2 (ruby 3.2.0), Xcode 16, macOS 15 Sequoia. No GitHub Releases/tags exist; track versions via npm only. Requires a custom dev client / EAS build — config plugins with native code do not run in Expo Go (general Expo constraint, not project-specific).

## `expo-target.config.js` / `.json`

One file per subdirectory of a root `/targets` folder. CommonJS only (`require`) — ESM/TypeScript unsupported in this file. Full `Config` TS type (confirmed from source, no `template` or `capabilities` field exists): `type` (required), `name`, `displayName`, `bundleIdentifier`, `icon`, `frameworks`, `deploymentTarget`, `appleTeamId`, `entitlements`, `colors`, `images`, `exportJs`.

```js
/** @type {import('@bacons/apple-targets/app.plugin').Config} */
module.exports = {
  type: "share",                 // or "keyboard" — see Target types
  name: "my_share_ext",          // defaults to the directory name
  displayName: "My Share Ext",   // CFBundleDisplayName, defaults to `name`
  icon: "../assets/icon.png",
  frameworks: ["SwiftUI"],
  deploymentTarget: "15.1",      // defaults to 18.0 if omitted
  bundleIdentifier: ".myshare",  // leading "." => appended to main app's bundle id
  entitlements: {
    "com.apple.security.application-groups": ["group.com.example.myapp"],
  },
  exportJs: false,               // bundle+embed Metro JS; for App Clip/Share ext using RN
};
```
A function form `module.exports = (config) => ({...})` receives the resolved Expo config, used to read the main app's App Group array (avoids duplicating the identifier string).

**Target types**: 45 types documented in the README table (46th, `imessage`, exists in source but is excluded from the visible table/CLI). Relevant here: `share` (Share Extension) and `keyboard` (Custom Keyboard Extension). Not yet supported by the plugin: `com.apple.tv-top-shelf`, `com.apple.FinderSync`, `com.apple.email.extension`.

## Build workflow

```sh
npx create-target <type>          # scaffolds targets/<name>/, installs the plugin
npx expo prebuild -p ios --clean  # generates ios/, links targets/<name>/ into Xcode
```
Target source lives in `targets/<name>/` (version-controlled) and is **linked**, not copied, into the generated `ios/` project — pure Swift-file edits need no prebuild. `--clean` is required after: initial target creation, any `expo-target.config.js` change (icon/colors/entitlements/bundle id/frameworks), any `app.json` plugin-config change, or adding/removing targets.

**Known open bugs in non-`--clean` incremental prebuild (as of 2026-09-01, unaddressed):**
- Issue #201: updating an *existing* target via plain `expo prebuild` (no `--clean`) can throw `TypeError: ... Cannot read properties of undefined (reading 'removeFromProject')` and fail outright; a clean prebuild succeeds. Filed 2026-06-09.
- Issue #202: `app-intent` targets specifically get duplicated on every non-clean prebuild (ExtensionKit product-type matching bug — `isNativeTargetOfType` never matches them, so a fresh duplicate target is created each run). Filed 2026-07-12.
- Issue #155: an Xcode 15+/16 `PBXFileSystemSynchronizedRootGroup` bug can break `prebuild --clean`/`pod install` outright; workaround is to remove the plugin from `app.json`, prebuild once, then re-add it.
Practical rule: prefer `--clean` whenever a target's config changed, not only for the cases the README lists as mandatory — incremental prebuild is reliable for pure code edits inside an already-generated target, less so for anything touching the target's Xcode-level definition.
- Issue #144 (SDK 52->54) and #196 (SDK 56, min iOS raised to 16.4 vs this plugin's 15.1/18.0 default) show each new Expo SDK major has required plugin-side fixes rather than being automatically compatible — check open issues before upgrading Expo SDK on a project using this plugin.

## App Groups (both sides)

Entitlement `com.apple.security.application-groups` (list of `group.`-prefixed strings), added via Xcode Signing & Capabilities on **both** the host app target and the extension target with the **identical** identifier string (case-sensitive; `group.` prefix mandatory or signing fails). Naming convention: `group.<bundle-identifier>`. Group IDs are global to the team and cannot be deleted once registered.

**Plugin auto-sync — exact type list**: for target types `widget`, `share`, `bg-download`, `clip`, `watch-widget`, `keyboard`, `file-provider`, `wallet`, `wallet-ui`, the plugin automatically copies the main app's App Group array into the extension's entitlements (checks an `appGroupsByDefault` flag per target type in `packages/apple-targets/src/target.ts`'s `TARGET_REGISTRY`, consumed by `with-widget.ts`) *unless* you define `entitlements["com.apple.security.application-groups"]` yourself. **`keyboard` is in this auto-sync list** (current 5.0.0 source) — a keyboard target inherits the main app's App Groups automatically with no config needed; only a type *not* on this list (e.g. `notification-content`, `intent`) needs an explicit `entitlements` block to get App Groups at all. Note: the plugin's own bundled skill doc (`skills/apple-targets/entitlements/app-groups.md`) still lists only `widget`/`share`/`clip`/`bg-download` — that doc is stale relative to `target.ts` as actually shipped; trust the source over it.

Data is never auto-migrated: adding the entitlement to a shipped app does not move existing data into the shared container. The container itself survives uninstall of any one app sharing the group; it is deleted only when the last app/extension using it is removed.

### Data hand-off APIs
- `UserDefaults(suiteName: String?)` — suite name must exactly equal one of the entitlement's group strings (iOS 7.0+).
- `FileManager.default.containerURL(forSecurityApplicationGroupIdentifier: String) -> URL?` — nil on iOS if the identifier is invalid; on macOS a URL is returned even for an invalid group, so verify access before use (iOS 7.0+).
- JS-side helper shipped by the plugin (wraps `NSUserDefaults`, no hand-written bridge module needed):
```js
import { ExtensionStorage } from "@bacons/apple-targets";
const storage = new ExtensionStorage("group.com.example.myapp");
storage.set("myKey", "myValue");   // string | number | Record<string, string|number> | Array<...> | undefined (removes key)
storage.get("myKey");              // static: string | null
ExtensionStorage.reloadWidget();   // WidgetCenter.shared.reloadAllTimelines()
```

## Share extension (`share`)

- Content arrives as `extensionContext.inputItems: [NSExtensionItem]`; each item's `attachments: [NSItemProvider]` is loaded async by UTI via `loadItem(forTypeIdentifier:options:)` (`public.url`, `public.image`, `public.plain-text`, ...). Must call `extensionContext?.completeRequest(returningItems:completionHandler:)` to dismiss.
- UI: subclass `SLComposeServiceViewController` (built-in compose UI) or provide a custom `UIViewController`. Custom SwiftUI via `UIHostingController` is architecturally standard but **not Apple-documented for this extension type specifically** (see Unverified).
- **Network access is available by default** — unlike keyboard extensions, share extensions have no `RequestsOpenAccess`/Full-Access gate in Apple's docs. Some MDM configurations can still restrict it.
- `NSExtensionActivationRule` (Info.plist, `NSExtension > NSExtensionAttributes`): `NSExtensionActivationSupportsText` (Bool), `NSExtensionActivationSupportsImageWithMaxCount` (Int), `NSExtensionActivationSupportsWebURLWithMaxCount` (Int), `NSExtensionActivationSupportsWebPageWithMaxCount` (Int). A bare predicate string is also accepted as the whole `NSExtensionActivationRule` value (compiled to `NSPredicate` at runtime) for cases the dictionary form can't express. **Shipping the default `TRUEPREDICATE` gets the app rejected on submission** — Apple's own guidance is explicit about this.
- Memory: no exact number is published in current official Apple docs — only that extensions get "a much lower per-process memory limit than foreground apps," device-dependent, jetsam-terminated on overage (confirmed absent from the jetsam event-report doc and, independently, from the full transcript of WWDC 2018 session 416 "iOS Memory Deep Dive," which discusses extension memory only in general terms). A widely repeated **~120 MB** figure (also stated by this plugin's own bundled skill doc, as an unqualified "hard cap") traces to third-party blog posts, not Apple. A cited developer-forums thread (Oct 2025) claiming a DTS engineer declined to confirm a number sits behind Apple's bot-check wall and could not be independently re-verified — re-check that specific thread before relying on it, or drop the citation and lean on the confirmed absence of any official figure instead. Do not hard-code 120 MB as a budget; test on-device.
- `exportJs: true` in `expo-target.config.js` is specifically meant for using React Native inside a Share Extension (or App Clip) target — it links the main target's JS-bundling build phase into the extension.
- The extension process can be killed at any time once `completeRequest` returns — anything that must survive that (large uploads) needs a background `URLSession`; a synchronous call awaited *before* `completeRequest` is the realistic pattern for something like a short LLM request, with no Apple-documented grace-period guarantee either way.

## Keyboard extension (`keyboard`)

- Subclasses `UIInputViewController`; UI goes in `inputView` (plain `UIViewController` subclass, so `UIHostingController`-based SwiftUI is architecturally standard but likewise **not Apple-documented for this extension type**). Insert/delete text via `textDocumentProxy.insertText(_:)` / `.deleteBackward()`; `documentContextBeforeInput`/`AfterInput` return only a limited surrounding-text window.
- `RequestsOpenAccess` (Info.plist Bool, default `false`): only takes effect once the user separately enables "Allow Full Access" in Settings for that keyboard. **Without it**: no network access, read-only (not write) access to the containing app's shared App Group container, no iCloud/Game Center/IAP, no Location Services/Contacts.
- **No microphone or camera access ever, Full Access or not** — Apple states this unconditionally for keyboard extensions; `hasDictationKey` only hides/shows the *system* dictation button in your UI, it grants no microphone capability.
- Memory: same as share extensions — no official number. A commonly cited **~40-50 MB** (some sources ~48 MB) is uncited community folklore; a targeted check of the WWDC session most often credited for "48 MB" (WWDC 2018 #416) found no such figure in its transcript.
- Globe/next-keyboard button is mandatory unless `needsInputModeSwitchKey` is `false` (true system globe key present, Face ID devices) — omitting it when required is an App Store rejection reason. Wire it to `handleInputModeList(from:with:)` on `.allTouchEvents`.
- A host app can force the system keyboard and block yours entirely: `application(_:shouldAllowExtensionPointIdentifier:)` returning `false`. Secure text fields (`isSecureTextEntry == true`) always fall back to the system keyboard regardless.
- No default height API — set a height constraint (`.defaultHigh` priority) on `view`/`inputView`; system default is ~216pt on iPhone.
- App Groups **are** auto-synced for `keyboard` targets by default (see App Groups section) — no explicit `entitlements` block is needed unless the keyboard should use a *different* App Group than the main app.

## Opening the host app from an extension

`NSExtensionContext.open(_:completionHandler:)` is real (iOS 8.0+, both a completion-handler and an `async` overload) but Apple scopes it explicitly: **"In iOS, the Today and iMessage app extension points support this method."** Share and keyboard extensions are not on that list. `UIApplication.shared` is unavailable inside any extension (enforced by the `@available(iOSApplicationExtension, unavailable)` compiler attribute; stated in prose only in Apple's archived, 2017-dated App Extension Programming Guide, not restated on current API reference pages). The widely-used "walk `UIResponder.next` until something responds to `openURL:`" workaround has **no Apple documentation or sample code** behind it anywhere found — treat it as an undocumented, unsupported workaround, not a sanctioned API (see Unverified).

Practical consequence for a share/keyboard extension that needs the host app's help (e.g. running a full AI generation flow): there is no direct-open API for either extension type. The reliable pattern is App-Group hand-off — write results to the shared container/`UserDefaults` and let the host app pick them up on next foreground/`scenePhase` change — not a forced app-switch.

## EAS Build signing

CNG projects declare every extension target via `extra.eas.build.experimental.ios.appExtensions` in the resolved Expo config — Expo's own docs label this **"CNG projects (experimental support)"** (page last updated 2026-06-26):
```json
{ "targetName": "myext", "bundleIdentifier": "com.myapp.extension", "entitlements": { "...": "..." } }
```
EAS CLI reads this *before* the Xcode project exists so it can generate/validate credentials up front. `@bacons/apple-targets` populates this array automatically after `expo prebuild`, scanning the generated Xcode project for each target's bundle id and entitlements (source: `with-eas-credentials.ts`). For **existing** (non-CNG) RN projects, EAS auto-detects extensions already in the Xcode project, or reads `credentials.json`.

Confidence check: the plugin's own README hedges this ("theoretically handled entirely by EAS Build... I've only tested this end-to-end with my Pillar Valley Widget... I haven't gotten App Clip codesigning to be fully automated yet"), while a newer bundled skill doc claims "No manual Apple Developer Portal work required" — the two are not reconciled in the repo. A real, open issue (#111) shows the automation has gaps: `com.apple.developer.parent-application-identifiers` (auto-set for App Clips) is silently skipped by `eas credentials` ("Skipping entitlement that is not supported by EAS"), then Apple's API rejects the request with a missing-`parentBundleId` error — evidence that not every entitlement this plugin emits is covered by EAS's automatic flow.

## Common failure modes

- **Bundle id**: when no `bundleIdentifier` is set, the extension bundle id actually defaults to `<main app bundle id>.<sanitized target TYPE>` (e.g. `.share`, `.keyboard`) — **not** the target's `name`/directory, despite the plugin's own README and `config.ts` doc comment both claiming "+ name" (verified against `with-widget.ts`'s actual generation code: `getSanitizedBundleIdentifier(props.type)`; `clip` targets are a special case defaulting to `.clip`). Two same-type targets (e.g. two `widget` targets) with no explicit `bundleIdentifier` will collide — always set `bundleIdentifier` explicitly if you have more than one target of the same type. A leading `.` in an explicit `bundleIdentifier` appends to the main app's id instead of replacing it. App Clips specifically require `com.apple.developer.parent-application-identifiers` = `$(AppIdentifierPrefix)<main bundle id>` (plugin sets this automatically).
- **Entitlement mismatch across targets breaks EAS signing**: if the main app has `["group.A","group.B"]` and an extension only has `["group.A"]`, EAS provisions only what's declared per target — correct, but easy to forget to re-sync (`prebuild --clean`) after editing one target's entitlements.
- **Non-clean prebuild after an existing target changes** can crash or duplicate targets (see Build workflow bugs above) — this is a materially bigger risk than "just re-run prebuild," despite the README's framing of non-clean prebuild as generally safe.
- **`UserDefaults` suite/App-Group string typos are silent** — a mismatched string creates a separate, unshared defaults store with no error.

## iOS 26 / Xcode 26 status (as of 2026-09-01)

Current shipping: iOS/iPadOS 26.6.1 (2026-08-17), Xcode 26.6. iOS 27 is in public beta (Beta 8 as of late August 2026), not GA — no confirmed primary-source GA date. **Nothing extension-specific changed for Share or Custom Keyboard extensions in iOS 26 / Xcode 26**: `NSExtensionContext`, `UIInputViewController`, the App Groups entitlement, and `UserDefaults` suite-sharing all show no iOS-26-dated members; release-note keyword sweeps (iOS 26.0/26.6, Xcode 26.0/26.6) found nothing for "extension," "keyboard," "share," "App Group," or "entitlement." Apple's current Share Extension overview still links to the archived (2017) programming guide, while Custom Keyboard links to a current, maintained guide — Share Extensions specifically have had no documentation refresh. The one iOS-26-era addition touching extension UI generally is `UIDesignRequiresCompatibility` (Info.plist Bool, opt out of automatic Liquid Glass styling; Apple states it stops working once building against the iOS 27 SDK) — a per-bundle key, so it would need setting in the extension's own Info.plist, though Apple's docs don't call out extensions specifically.

## Unverified (searched, not confirmed on any primary source — do not present as fact)

- Exact numeric memory limits (MB) for share or keyboard extensions in any current official Apple documentation.
- Any Apple sample code, guide, or WWDC session describing/endorsing the `UIResponder.next`-walk technique for opening a host app from a share or keyboard extension.
- Any Apple documentation or sample code pairing a Share Extension or Keyboard Extension with SwiftUI/`UIHostingController` specifically (generically supported, never shown for these two extension types).
- Whether keyboard-extension microphone/dictation access is possible under any special condition (MDM, entitlement, etc.) — current docs state the restriction with no listed exceptions, but also don't explicitly rule out every possible case.
- A primary-source iOS 27 GA date.
- Why `peerDependencies.expo` (`>=52`) and the plugin README's prose minimum ("+53") disagree.

## Sources

- https://raw.githubusercontent.com/EvanBacon/expo-apple-targets/main/packages/apple-targets/README.md
- https://raw.githubusercontent.com/EvanBacon/expo-apple-targets/main/packages/apple-targets/src/config.ts
- https://raw.githubusercontent.com/EvanBacon/expo-apple-targets/main/skills/apple-targets/share.md
- https://raw.githubusercontent.com/EvanBacon/expo-apple-targets/main/skills/apple-targets/keyboard.md
- https://raw.githubusercontent.com/EvanBacon/expo-apple-targets/main/skills/apple-targets/entitlements/app-groups.md
- https://github.com/EvanBacon/expo-apple-targets/issues/111
- https://github.com/EvanBacon/expo-apple-targets/issues/144
- https://github.com/EvanBacon/expo-apple-targets/issues/155
- https://github.com/EvanBacon/expo-apple-targets/issues/196
- https://github.com/EvanBacon/expo-apple-targets/issues/201
- https://github.com/EvanBacon/expo-apple-targets/issues/202
- https://registry.npmjs.org/@bacons/apple-targets and https://registry.npmjs.org/create-target
- https://docs.expo.dev/build-reference/app-extensions/
- https://docs.expo.dev/workflow/continuous-native-generation/
- https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.security.application-groups
- https://developer.apple.com/documentation/foundation/userdefaults/init(suitename:)
- https://developer.apple.com/documentation/foundation/filemanager/containerurl(forsecurityapplicationgroupidentifier:)
- https://developer.apple.com/documentation/bundleresources/information-property-list/nsextension/nsextensionattributes/nsextensionactivationrule
- https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/ExtensionScenarios.html
- https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/CustomKeyboard.html
- https://developer.apple.com/documentation/uikit/creating-a-custom-keyboard
- https://developer.apple.com/documentation/uikit/configuring-open-access-for-a-custom-keyboard
- https://developer.apple.com/documentation/foundation/nsextensioncontext/open(_:completionhandler:)
- https://developer.apple.com/documentation/xcode/identifying-high-memory-use-with-jetsam-event-reports
- https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-26-release-notes
- https://developer.apple.com/documentation/ios-ipados-release-notes/ios-ipados-27-release-notes
- https://developer.apple.com/documentation/xcode-release-notes/xcode-26-release-notes
- https://developer.apple.com/documentation/technologyoverviews/app-extensions
- https://developer.apple.com/documentation/bundleresources/information-property-list/uidesignrequirescompatibility
